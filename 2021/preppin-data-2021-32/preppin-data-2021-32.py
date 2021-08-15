# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 32- Excelling through Aggregation
https://preppindata.blogspot.com/2021/08/2021-week-32-excelling-through.html

- Input data
- Form Flight name
- Workout how many days between the sale and the flight departing
- Classify daily sales of a flight as:
  - Less than 7 days before departure
  - 7 or more days before departure
- Mimic the SUMIFS and AverageIFS functions by aggregating the previous requirements fields by each
  Flight and Class
- Round all data to zero decimal places
- Output the data

Author: Kelly Gilbert
Created: 2021-08-15
Requirements:
  - input dataset:
      - PD 2021 Wk 32 Input - Data.csv
  - output dataset (for results check only):
      - PD 2021 Wk 32 Output.csv
"""


from numpy import nan, where
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\\inputs\\PD 2021 Wk 32 Input - Data.csv', parse_dates=['Date', 'Date of Flight'], 
              dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# form flight name
df['Flight'] = df['Departure'] + ' to ' + df['Destination']

# days between the sale and the flight date
df['days'] = (df['Date of Flight'] - df['Date']).dt.days

# classify as less than 7 / 7 or more days before departure
df['sales_lt_7'] = where(df['days'] < 7, df['Ticket Sales'], nan)
df['sales_gte_7'] = where(df['days'] < 7, nan, df['Ticket Sales'])

# sum and average by day classification
df_tot = df.groupby(['Flight', 'Class']).agg(avg_gte_7=('sales_gte_7', 'mean'),
                                             avg_lt_7=('sales_lt_7', 'mean'),
                                             sum_lt_7=('sales_lt_7', 'sum'),
                                             sum_gte_7=('sales_gte_7', 'sum'))\
           .round(0).astype(int)\
           .reset_index()
           
renames = { 'avg_gte_7' : 'Avg. daily sales 7 days or more until the flight',
            'avg_lt_7' : 'Avg. daily sales less than 7 days until the flight',
            'sum_lt_7' : 'Sales less than 7 days until the flight',
            'sum_gte_7' : 'Sales 7 days or more until the flight' }

df_tot.rename(columns=renames, inplace=True)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_tot.to_csv(r'.\outputs\output-2021-32.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 32 Output.csv']
my_files = ['output-2021-32.csv']
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
