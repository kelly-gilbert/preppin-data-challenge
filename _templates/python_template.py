# -*- coding: utf-8 -*-
"""
Preppin' Data YYYY: Week WW - challenge title goes here
https://preppindata.blogspot.com/ - challenge url goes here

- Input data
- ...
- Output the data

Author: Kelly Gilbert
Created: YYYY-MM-DD
Requirements:
  - input dataset:
      - 
  - output dataset (for results check only):
      - 
"""


from pandas import read_csv

# for results check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'', parse_dates=[], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-YYYY-WW.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['']
my_files = ['output-YYYY-WW.csv']
unique_cols = ['Month']
col_order_matters = True
round_dec = 8


for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_sol = read_csv('.\\outputs\\' + solution_file)
    df_mine = read_csv('.\\outputs\\' + my_files[i])

    # are the columns the same?
    solution_cols = list(df_sol.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_sol.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
        print('\n\n')
    else:
        print('Columns match\n')
        col_match = True


    # are the values the same? (only check if the columns matched)
    if col_match:
        df_compare = df_sol.merge(df_mine, how='outer', on=unique_cols,
                                  suffixes=['_sol', '_mine'], indicator=True)
        
        # extra/missing records
        if len(df_compare[df_compare['_merge'] != 'both']) > 0:
            print('*** Missing or extra records ***\n')
            print('In solution, not in mine:\n')
            print(df_compare[df_compare['_merge'] == 'left_only'][unique_cols])
            print('\n\nIn mine, not in solution:\n')
            print(df_compare[df_compare['_merge'] == 'right_only'][unique_cols]) 


        # for the records that matched, check for mismatched values
        unmatched_cols = 0
        for c in [c for c in df_sol.columns if c not in unique_cols]:
            if 'float' in df_compare[f'{c}_sol'].dtype.name:
                df_compare[f'{c}_sol'] = df_compare[f'{c}_sol'].round(round_dec)
                df_compare[f'{c}_mine'] = df_compare[f'{c}_mine'].round(round_dec)
                
            unmatched = df_compare[(df_compare['_merge']=='both')
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]
            if len(unmatched) > 0:
                print(f'*** Values do not match: {c} ***\n')
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                unmatched_cols += 1
        
        if unmatched_cols == 0:
            print('Values match')

    print('\n')  
