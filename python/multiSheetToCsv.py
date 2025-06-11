import pandas as pd

# Read Excel file into a Pandas ExcelFile object
xls = pd.ExcelFile('Copy of THE TCS SHOPPING LIST for LC.xlsx')

# drop Template sheet
del xls.book['Template']

combined_df = pd.DataFrame([], columns=["ITEM","IMAGE","DIMENSIONS","SKU","PRICE","QUANITY","TOTAL","ROOM"])

# Iterate through each sheet in the Excel file
for sheet_name in xls.sheet_names:
    # Read the sheet into a DataFrame
    df = pd.read_excel(xls, sheet_name)
    
    df['ROOM'] = sheet_name

    df.columns = df.columns.str.replace(' ', '')
    df.columns = df.columns.str.replace('#', '')

    combined_df = pd.concat([combined_df, df])
    combined_df.to_csv(f'sheets/_combined.csv', index=False)

    # Export the DataFrame to a CSV file
    df.to_csv(f'sheets/{sheet_name.strip()}.csv', index=False)