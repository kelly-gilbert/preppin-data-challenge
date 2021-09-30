# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 39 - Painting Bikes
https://preppindata.blogspot.com/2021/09/2021-week-39-painting-bikes.html

- Input the Data
- Create a Datetime field
- Parse the Bike Type and Batch Status for each batch
- Parse the Actual & Target values for each parameter. 
- Identify what time each of the different process stage's took place. Each process stage is
  provided with a start time, and there is no overlap between stages. Assume that the final process
  stage ends when the last update occurs.
- Output the data in a single table.

Author: Kelly Gilbert
Created: 2021-09-29
Requirements:
  - input dataset:
      - Bike Painting Process - Painting Process.csv
  - output dataset (for results check only):
      - 2021 Week 39 Output.csv
"""

from numpy import nan, where
from pandas import merge, pivot_table, read_csv, Series


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\\inputs\\Bike Painting Process - Painting Process.csv',
              parse_dates={'Datetime' : ['Date', 'Time']}, dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# parse the Bike Type and Batch Status for each batch
df_batch = pivot_table(df[df['Data Parameter'].isin(['Bike Type', 'Batch Status'])],
                       values='Data Value', index=['Batch No.'], columns='Data Parameter',
                       aggfunc=max).reset_index()

# fill down the process step
df = df.sort_values(['Batch No.', 'Datetime'])
df['Name of Process Step'] = Series(where(df['Data Parameter']=='Name of Process Stage', 
                                          df['Data Value'], nan)).fillna(method='ffill')


# parse the Actual & Target values for each parameter. 
df[['Parameter Type', 'Data Parameter']] = df['Data Parameter'].str.extract('(Actual|Target)? ?(.*)')
df_parms = pivot_table(df, values='Data Value', columns='Parameter Type', aggfunc=max,
                       index=['Batch No.', 'Name of Process Step', 'Datetime', 'Data Parameter'])\
           .reset_index()


# join the batch data and the parm data
df_final = df_batch.merge(df_parms, on='Batch No.')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Batch No.', 'Name of Process Step', 'Bike Type', 'Batch Status', 'Datetime', 
            'Data Parameter', 'Target', 'Actual']
df_final.to_csv(r'.\outputs\output-2021-39.csv', index=False, date_format='%d/%m/%Y %H:%M:%S',
                columns=out_cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['2021 Week 39 Output.csv']
my_files = ['output-2021-39.csv']
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
