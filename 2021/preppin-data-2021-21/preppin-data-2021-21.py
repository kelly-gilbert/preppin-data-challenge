# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 20 - Getting Trolleyed
https://preppindata.blogspot.com/2021/05/2021-week-21-getting-trolleyed.html

- Input data
- Bring all the sheets together
- Use the Day of Month and Table Names (sheet name in other tools) to form a date field for the
  purchase called 'Date'
- Create 'New Trolley Inventory?' field to show whether the purchase was made on or after
  1st June 2021 (the first date with the revised inventory after the project closed)
- Remove lots of the detail of the product name:
    - Only return any names before the '-' (hyphen)
    - If a product doesn't have a hyphen return the full product name
- Make price a numeric field
- Work out the average selling price per product
- Workout the Variance (difference) between the selling price and the average selling price
- Rank the Variances (1 being the largest positive variance) per destination and whether the product
  was sold before or after the new trolley inventory project delivery
- Return only ranks 1-5
- Output the data

Author: Kelly Gilbert
Created: 2021-06-01
Requirements:
  - input dataset:
      - PD 2021 Wk 21 Input.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 21 Output.csv
"""

from datetime import datetime
from pandas import concat, DataFrame, ExcelFile, read_excel, to_datetime

# for solution check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = None
with ExcelFile(r'.\\inputs\\PD 2021 Wk 21 Input.xlsx') as xl:
    for s in xl.sheet_names:
        df_new = read_excel(xl, s)
        df_new['sheet_name'] = s
        df = concat([df, df_new])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# trim the Destination
df['Destination'] = df['Destination'].str.strip()

# Use the Day of Month and Table Names (sheet name in other tools) to form a date field
df['Date'] = to_datetime('2021' + '-' + df['sheet_name'].str.replace('Month ', '')
                         + '-' + df['Day of Month'].astype(str))

# Create 'New Trolley Inventory?' field to show whether the purchase was made on or after 6/1/2021
df['New Trolley Inventory?'] = (df['Date'] >= datetime(2021, 6, 1))

# parse the product type before the hyphen
df['Product'] = df['Product'].str.split(' -').str[0]

# make price a numeric field
df['Price'] = df['Price'].str.strip('$').astype(float)

# work out the average selling price per product
df['Avg Price per Product'] = df.groupby('Product')['Price'].transform('mean')

# work out the Variance (difference) between the selling price and the average selling price
df['Variance'] = df['Price'] - df['Avg Price per Product']

# rank the Variances (1 being the largest positive variance) per destination and whether the product
# was sold before or after the new trolley inventory project delivery
df['Variance Rank by Destination'] = df.groupby(['Destination', 'New Trolley Inventory?'])\
                                       ['Variance'].rank(ascending=False).astype(int)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# return only ranks 1-5
out_cols = ['New Trolley Inventory?', 'Variance Rank by Destination', 'Variance',
            'Avg Price per Product', 'Date', 'Product', 'first_name', 'last_name', 'email',
            'Price', 'Destination']
df[df['Variance Rank by Destination'] <= 5].to_csv(r'.\outputs\output-2021-21.csv', index=False,
                                                   columns=out_cols, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 21 Output.csv']
my_files = ['output-2021-21.csv']
col_order_matters = False

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_file)
    df_mine = read_csv('.\\outputs\\' + my_files[i])

    # are the fields the same and in the same order?
    solution_cols = list(df_solution.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_solution.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        # round float values
        s = df_solution.dtypes.astype(str)
        for c in s[s.str.contains('float')].index:
            df_solution[c] = df_solution[c].round(8)
            df_mine[c] = df_mine[c].round(8)

        # join the dataframes on all columns except the in flags
        df_solution['in'] = 1
        df_mine['in'] = 1
        df_solution_compare = df_solution.merge(df_mine, how='outer',
                                                on=list(df_solution.columns)[:-1],
                                                suffixes=['_solution', '_mine'])

        if df_solution_compare['in_solution'].count() != len(df_solution_compare):
            print('*** Values do not match ***')
            print(df_solution_compare[df_solution_compare['in_solution'] 
                                      != df_solution_compare['in_mine']])
        else:
            print('Values match')

    print('\n')
