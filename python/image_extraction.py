import zipfile
import os
import re
import xml.etree.ElementTree as ET
import pandas as pd

NS = {
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'xdr': 'http://schemas.openxmlformats.org/drawingml/2006/spreadsheetDrawing',
    'main': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main',
}

def get_sheet_id_map(zipf):
    sheet_id_map = {}
    with zipf.open('xl/workbook.xml') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        sheets = root.find('main:sheets', NS)
        for sheet in sheets.findall('main:sheet', NS):
            rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
            name = sheet.attrib['name']
            sheet_id_map[rid] = name
    return sheet_id_map

def get_rels(zipf, path):
    rels = {}
    try:
        with zipf.open(path) as f:
            tree = ET.parse(f)
            root = tree.getroot()
            for rel in root.findall('{http://schemas.openxmlformats.org/package/2006/relationships}Relationship'):
                rid = rel.attrib['Id']
                target = rel.attrib['Target']
                rels[rid] = target
    except KeyError:
        pass
    return rels

def col_row_to_cell(col, row):
    col_str = ''
    while col >= 0:
        col_str = chr(ord('A') + (col % 26)) + col_str
        col = col // 26 - 1
    return f"{col_str}{row+1}"

def parse_drawing(zipf, drawing_path, rels, sheet_name):
    images = []
    with zipf.open(drawing_path) as f:
        tree = ET.parse(f)
        root = tree.getroot()
        anchors = root.findall('xdr:twoCellAnchor', NS) + root.findall('xdr:oneCellAnchor', NS)
        for anchor in anchors:
            from_elem = anchor.find('xdr:from', NS)
            if from_elem is None:
                continue
            col = int(from_elem.find('xdr:col', NS).text)
            row = int(from_elem.find('xdr:row', NS).text)
            cell = col_row_to_cell(col, row)
            pic = anchor.find('xdr:pic', NS)
            if pic is None:
                continue
            blip = pic.find('.//a:blip', NS)
            if blip is None:
                continue
            embed = blip.attrib.get(f'{{{NS["r"]}}}embed')
            if not embed:
                continue
            image_path = rels.get(embed)
            if not image_path:
                continue
            image_file = os.path.basename(image_path)
            images.append({'sheet': sheet_name, 'image': image_file, 'cell': cell, 'row': row})
    return images

def extract_skus_from_sheet(zipf, sheet_file):
    try:
        with zipf.open(f"xl/{sheet_file}") as f:
            tree = ET.parse(f)
            root = tree.getroot()
            rows = root.findall('.//main:row', NS)
            sku_map = {}
            for row in rows:
                row_num = int(row.attrib['r']) - 1
                for c in row.findall('main:c', NS):
                    cell_ref = c.attrib['r']
                    col_letter = re.match(r"[A-Z]+", cell_ref).group()
                    if col_letter in ['C', 'D']:  # assume SKU is in column C or D
                        v = c.find('main:v', NS)
                        if v is not None:
                            sku_map[row_num] = v.text
            return sku_map
    except Exception:
        return {}

def extract_images_with_positions(xlsx_path, output_folder='extracted_images'):
    os.makedirs(output_folder, exist_ok=True)
    images_info = []

    with zipfile.ZipFile(xlsx_path) as zipf:
        sheet_id_map = get_sheet_id_map(zipf)
        wb_rels = get_rels(zipf, 'xl/_rels/workbook.xml.rels')
        sheet_file_to_name = {}

        with zipf.open('xl/workbook.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()
            sheets = root.find('main:sheets', NS)
            for sheet in sheets.findall('main:sheet', NS):
                rid = sheet.attrib['{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id']
                name = sheet.attrib['name']
                sheet_file = wb_rels.get(rid)
                if sheet_file:
                    sheet_file_to_name[sheet_file] = name

        for sheet_file, sheet_name in sheet_file_to_name.items():
            sheet_rels_path = f"xl/worksheets/_rels/{os.path.basename(sheet_file)}.rels"
            sheet_rels = get_rels(zipf, sheet_rels_path)

            drawing_target = None
            for rid, target in sheet_rels.items():
                if 'drawings/drawing' in target:
                    drawing_target = 'xl/' + target.replace('../', '')
                    break
            if not drawing_target:
                continue

            drawing_rels_path = f"xl/drawings/_rels/{os.path.basename(drawing_target)}.rels"
            drawing_rels = get_rels(zipf, drawing_rels_path)

            imgs = parse_drawing(zipf, drawing_target, drawing_rels, sheet_name)

            sku_map = extract_skus_from_sheet(zipf, sheet_file)
            for img in imgs:
                img['sku'] = sku_map.get(img['row'], None)

            images_info.extend(imgs)

        media_files = [f for f in zipf.namelist() if f.startswith('xl/media/')]
        media_files_set = set(os.path.basename(f) for f in media_files)

        for img in images_info:
            img_file = img['image']
            if img_file not in media_files_set:
                continue
            img_path_in_zip = f"xl/media/{img_file}"
            target_path = os.path.join(output_folder, img_file)
            with open(target_path, 'wb') as f_out:
                f_out.write(zipf.read(img_path_in_zip))
            img['extracted_path'] = target_path

    return images_info

def main():
    xlsx_path = 'products.xlsx'
    output_folder = 'extracted_images'
    images_info = extract_images_with_positions(xlsx_path, output_folder)

    if not images_info:
        print("❌ No images with position info found.")
        return

    df = pd.DataFrame(images_info)
    df = df[['sheet', 'cell', 'sku', 'image', 'extracted_path']]
    df.to_csv('image_cell_mapping.csv', index=False)
    print(f"✅ Extracted {len(images_info)} images and saved mapping (with SKU) to 'image_cell_mapping.csv'")

if __name__ == '__main__':
    main()
