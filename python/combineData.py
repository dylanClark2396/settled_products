import pandas as pd
import re
from fractions import Fraction
import os

def clean_dimension_part(part):
    if pd.isna(part):
        return None
    part = str(part).lower().strip()
    part = re.sub(r'[a-z\s]+$', '', part)
    part = part.replace('"', '').replace('”', '').replace('“', '')
    part = re.sub(r'(\d+)-(\d+/\d+)', r'\1 \2', part)
    return part.strip()

def parse_fraction(value_str):
    if value_str is None or value_str == '':
        return None
    parts = value_str.split()
    if len(parts) == 2:
        try:
            return float(parts[0]) + float(Fraction(parts[1]))
        except Exception:
            return None
    if '/' in value_str:
        try:
            return float(Fraction(value_str))
        except Exception:
            return None
    try:
        return float(value_str)
    except Exception:
        return None

def to_inches(value_str):
    if pd.isna(value_str):
        return None
    cleaned = clean_dimension_part(str(value_str).lower().strip())
    return parse_fraction(cleaned)

def split_dimensions(dim_str):
    try:
        dim_str = str(dim_str).lower()
        parts = re.split(r'\s*x\s*', dim_str)
        if len(parts) == 3:
            d = to_inches(parts[0])
            w = to_inches(parts[1])
            h = to_inches(parts[2])
            return pd.Series({'depth': d, 'width': w, 'height': h})
    except Exception:
        pass
    return pd.Series({'depth': None, 'width': None, 'height': None})

def sanitize_column_name(col):
    clean = re.sub(r'\W+', '_', str(col).strip().lower())
    clean = re.sub(r'_+', '_', clean)
    return clean.strip('_')

def combine_excel_sheets_to_csv(xlsx_file_path, output_csv_path, image_mapping_csv='image_cell_mapping.csv'):
    # Load image path mapping if available
    image_df = pd.read_csv(image_mapping_csv) if os.path.exists(image_mapping_csv) else pd.DataFrame()
    if not image_df.empty and 'sku' in image_df.columns:
        image_df['sku'] = image_df['sku'].astype(str).str.replace(r'\.0$', '', regex=True)

    all_sheets = pd.read_excel(xlsx_file_path, sheet_name=None)
    combined_df = []

    for sheet_name, df in all_sheets.items():
        if sheet_name.lower() == 'template':
            continue

        df = df.copy()
        df.columns = [sanitize_column_name(col) for col in df.columns]
        df = df.loc[:, ~df.columns.str.match(r'^unnamed_\d+$')]

        for col in df.columns:
            if re.fullmatch(r'sku_?', col):
                df.rename(columns={col: 'sku'}, inplace=True)
                break

        if 'sku' in df.columns:
            df['sku'] = df['sku'].astype(str).str.replace(r'\.0$', '', regex=True)

        df['room'] = sheet_name

        if 'dimensions' in df.columns:
            split_cols = df['dimensions'].apply(split_dimensions)
            df = pd.concat([df, split_cols], axis=1)

        if not image_df.empty and 'sku' in df.columns:
            df = df.merge(image_df[['sku', 'extracted_path']], on='sku', how='left')
            df.rename(columns={'extracted_path': 'image_path'}, inplace=True)

        combined_df.append(df)

    non_empty_dfs = [df for df in combined_df if not df.empty]
    final_df = pd.concat(non_empty_dfs, ignore_index=True)

    # Drop rows without images
    final_df = final_df.dropna(subset=['image_path'])

    # Drop unnecessary columns
    for col_to_drop in ['image', 'quanity', 'total']:
        if col_to_drop in final_df.columns:
            final_df.drop(columns=col_to_drop, inplace=True)

    final_df.to_csv(output_csv_path, index=False)
    print(f"✅ Combined CSV saved to: {output_csv_path}")

# Run the script
if __name__ == '__main__':
    combine_excel_sheets_to_csv('products.xlsx', 'combined_output.csv', 'image_cell_mapping.csv')
