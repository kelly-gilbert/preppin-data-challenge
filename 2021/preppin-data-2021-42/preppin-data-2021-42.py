# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 42 - Charity Fundraising
https://preppindata.blogspot.com/2021/10/2021-week-42-charity-fundraising.html

- Input the data
- Create new rows for any date missing between the first and last date in the data set provided
- Calculate how many days of fundraising there has been by the date in each row (1st Jan would be 0)
- Calculate the amount raised per day of fundraising for each row
- Workout the weekday for each date
- Average the amount raised per day of fundraising for each weekday
- Output the data

Author: Kelly Gilbert
Created: 2021-10-21
Requirements:
  - input dataset:
      - Prep Generate Rows datasets - Charity Fundraiser.csv
  - output dataset (for results check only):
      - 2021 Week 42 Output.csv
"""


from numpy import where    # only used for rounding the output
from pandas import DataFrame, date_range, read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_in = read_csv(r'.\\inputs\\Prep Generate Rows datasets - Charity Fundraiser.csv', 
                 parse_dates=['Date'], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create new rows for any date missing between the first and last date in the data set provided
# calculate how many days of fundraising there has been by the date in each row (1st Jan would be 0)
df = DataFrame({'Date' : date_range(start=df_in['Date'].min(), end=df_in['Date'].max(), freq='D')})\
     .merge(df_in, on='Date', how='left')\
     .reset_index().rename(columns={'index':'Days into fund raising'})


# calculate the amount raised per day of fundraising for each row
df['Total Raised to date'].fillna(method='ffill', inplace=True)
df['Value raised per day'] = (df['Total Raised to date'] / df['Days into fund raising']).round(9)


# workout the weekday for each date
df['Date'] = df['Date'].dt.day_name()


# average the amount raised per day of fundraising for each weekday
df['Avg raised per weekday'] = df.groupby('Date')['Value raised per day'].transform('mean').round(9)


#---------------------------------------------------------------------------------------------------
# formatting to match the solution file
#---------------------------------------------------------------------------------------------------

# this part isn't absolutely necessary; it was just an extra little challenge to match the 
# provided output file, which represents whole numbers without decimals (e.g. 50) and floats using
# smallest number of decimal places necessary (up to 9)

def apply_format(s):
    """
    formats a series of numbers as strings
        if nan --> empty string
        if whole number --> no decimal places
        otherwise --> 9 decimal places
    """
    
    return where(s.isna(), '', 
                 s.map(lambda x: f'{x:.0f}' if x == round(x, 0) else str(x)))


df['Value raised per day'] = apply_format(df['Value raised per day'])
df['Avg raised per weekday'] = apply_format(df['Avg raised per weekday'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2021-42.csv', index=False,
          columns=['Avg raised per weekday', 'Value raised per day', 'Days into fund raising', 
                   'Date', 'Total Raised to date'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['2021 Week 42 Output.csv']
my_files = ['output-2021-42.csv']
col_order_matters = True

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_file, keep_default_na=False)
    df_mine = read_csv('.\\outputs\\' + my_files[i], keep_default_na=False)

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
