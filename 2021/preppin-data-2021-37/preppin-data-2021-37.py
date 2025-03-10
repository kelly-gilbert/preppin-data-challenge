# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 37 - Re-looking at Phone Contract Revenue
https://preppindata.blogspot.com/2021/09/2021-week-37-re-looking-at-phone.html

- Input the Data
- Calculate the End Date for each contract
- Create a Row for each month a person will hold the contract
- Calculate the monthly cumulative cost of each person's contract
- Output the Data

Author: Kelly Gilbert
Created: 2021-09-24
Requirements:
  - input dataset:
      - 2021 Week 37 Input.xlsx
  - output dataset (for results check only):
      - 2021 Week 37 Output.csv
"""


from pandas import date_range, ExcelFile, read_excel
from pandas.tseries.offsets import DateOffset

# for answer check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_excel(ExcelFile(r'.\\inputs\\2021 Week 37 Input.xlsx'), 'Contract Details')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create a Row for each month a person will hold the contract
df['Payment Date'] = [date_range(d, periods=p, freq=DateOffset(months=1)) for d, p 
              in zip(df['Start Date'], df['Contract Length (months)'])]
df = df.explode('Payment Date')


# calculate the monthly cumulative cost of each person's contract
df['Cumulative Monthly Cost'] = df.groupby('Name')['Monthly Cost'].cumsum()


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2021-37.csv', index=False, date_format='%d/%m/%Y',
          columns=['Name', 'Payment Date', 'Monthly Cost', 'Cumulative Monthly Cost'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['2021 Week 37 Output.csv']
my_files = ['output-2021-37.csv']
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
