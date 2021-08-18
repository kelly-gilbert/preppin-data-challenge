# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 33 - Excelling at adding one more row
https://preppindata.blogspot.com/2021/08/2021-week-33-excelling-at-adding-one.html

- Input the data
- Create one complete data set
- Use the Table Names field to create the Reporting Date
- Find the Minimum and Maximum date where an order appeared in the reports
- Add one week on to the maximum date to show when an order was fulfilled by
- Apply this logic:
  - The first time an order appears it should be classified as a 'New Order'
  - The week after the last time an order appears in a report (the maximum date) is when the order is classed as 'Fulfilled' 
  - Any week between 'New Order' and 'Fulfilled' status is classed as an 'Unfulfilled Order' 
- Pull of the data sets together 
- Remove any unnecessary fields
- Output the data

Author: Kelly Gilbert
Created: 2021-08-18
Requirements:
  - input dataset:
      - Allchains Weekly Orders.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 33 Output.csv
"""


from numpy import where
from pandas import concat, ExcelFile, read_excel, Timedelta, to_datetime

# for results check only:
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = None
with ExcelFile(r'.\\inputs\\Allchains Weekly Orders.xlsx') as xl:
    for s in xl.sheet_names:
        df_temp = read_excel(xl, s)
        df_temp['sheet'] = s
        df = concat([df, df_temp])
        
        
#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create the Reporting Date
df['Reporting Date'] = to_datetime(df['sheet'].str[0:4] + '-' + df['sheet'].str[4:6] 
                                   + '-' + df['sheet'].str[6:])

# find the Minimum and Maximum date where an order appeared in the reports
df['first_date'] = df.groupby('Orders')['Reporting Date'].transform('min')
df['last_date'] = df.groupby('Orders')['Reporting Date'].transform('max')

# flag as new or unfulfilled
df['Order Status'] = where(df['Reporting Date']==df['first_date'], 'New Order', 'Unfulfilled Order')

# extract the fulfilled orders, and add one week to the maximum date
fulfilled = df.loc[(df['Reporting Date']==df['last_date']) 
                   & (df['Reporting Date'] != df['Reporting Date'].max())].copy()
fulfilled['Reporting Date'] = fulfilled['Reporting Date'] + Timedelta('7 day')
fulfilled['Order Status'] = 'Fulfilled'

# append the datasets and remove unnecessary fields
df = concat([df, fulfilled])[['Order Status', 'Orders', 'Sale Date', 'Reporting Date']]


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2021-33.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 33 Output.csv']
my_files = ['output-2021-33.csv']
col_order_matters = True

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
        df_solution_compare = df_solution.merge(df_mine, how='outer',
                                                on=list(df_solution.columns),
                                                suffixes=['_solution', '_mine'], indicator=True)

        if len(df_solution_compare[df_solution_compare['_merge'] != 'both']) > 0:
            print('*** Values do not match ***\n')
            print('In solution, not in mine:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'left_only']) 
            print('\n\n')
            print('In mine, not in solution:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'right_only']) 
            
        else:
            print('Values match')

    print('\n')
