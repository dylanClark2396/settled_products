import pandas as pd

# Read Excel file into a Pandas ExcelFile object
xls = pd.ExcelFile('Copy of THE TCS SHOPPING LIST for LC.xlsx')

# Iterate through each sheet in the Excel file
for sheet_name in xls.sheet_names:
    # Read the sheet into a DataFrame
    df = pd.read_excel(xls, sheet_name)
    # Export the DataFrame to a CSV file
    df.to_csv(f'sheets/{sheet_name}.csv', index=False)