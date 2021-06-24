# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 24 - C&BS Co Absence Monitoring
https://preppindata.blogspot.com/2021/06/2021-week-24-c-co-absence-monitoring.html

- Input data
- Build a data set that has each date listed out between 1st April to 31st May 2021
- Build a data set containing each date someone will be off work
- Merge these two data sets together 
- Workout the number of people off each day
- Output the data
- Can you answer:
    - What date had the most people off?
    - How many days does no-one have time off on?

Author: Kelly Gilbert
Created: 2021-06-16
Requirements:
  - input dataset:
      - Absenteeism Scaffold.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 24 Output.csv
"""


from datetime import datetime as dt
from pandas import DataFrame, date_range, ExcelFile, read_excel

# for solution check only
from pandas import read_csv


start_date = '2021-04-01'
end_date = '2021-05-31'


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Absenteeism Scaffold.xlsx') as xl:
    df = read_excel(xl, 'Reasons')
        

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# count of absences by date
df['Date'] = [date_range(d, periods=p, freq='D') for d, p in zip(df['Start Date'], df['Days Off'])]
df_count = df.explode('Date').groupby('Date')['Name'].count().reset_index()
df_count.rename(columns={'Name' : 'Number of people off each day'}, inplace=True)


# generate a list of days in the range of interest
df_dates = DataFrame({'Date' : date_range(start=start_date, end=end_date)})

# join to dates of interest and fill in zeroes
df_dates = df_dates.merge(df_count, on='Date', how='left').fillna(0)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_dates.to_csv(r'.\outputs\output-2021-24.csv', index=False, date_format='%d/%m/%Y %H:%M:%S')


#---------------------------------------------------------------------------------------------------
# questions
#---------------------------------------------------------------------------------------------------

# What date had the most people off?
max_date = df_dates.iloc[df_dates.iloc[:, 1].idxmax()]['Date']
print('Date with the most people off: ' + dt.strftime(max_date, '%d/%m/%Y'))

# How many days does no-one have time off on?
print('Days with no absences: ' + str(len(df_dates[df_dates.iloc[:, 1]==0])))


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 24 Output.csv']
my_files = ['output-2021-24.csv']
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
