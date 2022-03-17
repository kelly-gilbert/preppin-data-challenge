# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 11 - The Prep School - Filling the Blanks
https://preppindata.blogspot.com/2022/03/2022-week-11-prep-school-filling-blanks.html

- Input the data set
- Fill in the blanks 
- Find the average Attendance per Lesson and Subject per weekday
- Output the data

Author: Kelly Gilbert
Created: 2022-03-16
Requirements:
  - input dataset:
      - PD Fill the Blanks challenge.csv
  - output dataset (for results check only):
      - PD 2022 Wk 11 Output.csv
"""


import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\PD Fill the Blanks challenge.csv')\
       .rename(columns={'Lesson Time' : 'Time'})\
       .assign(Time=lambda df_x: df_x['Time'] + ':00')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# fill in the blanks (each lesson is taught at the same time, on the same day
df = df.sort_values(by=['Weekday', 'Time', 'Subject', 'Lesson Name'], ascending=False)\
       .ffill()

# find the average Attendance per Lesson and Subject per weekday
df['Avg. Attendance per Subject & Lesson'] = \
    df.groupby(['Subject', 'Lesson Name'])['Attendance'].transform('mean')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-11.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2022 Wk 11 Output.csv']
my_files = ['output-2022-11.csv']
unique_cols = [['Weekday', 'Week', 'Time']]
col_order_matters = False
round_dec = 8

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_sol = pd.read_csv('.\\outputs\\' + solution_file)
    df_mine = pd.read_csv('.\\outputs\\' + my_files[i])

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
        errors = 0
        df_compare = df_sol.merge(df_mine, how='outer', on=unique_cols[i],
                                  suffixes=['_sol', '_mine'], indicator=True)
        
        # extra/missing records
        if len(df_compare[df_compare['_merge'] != 'both']) > 0:
            print('\n\n*** Missing or extra records ***')
            print('\n\nIn solution, not in mine:\n')
            print(df_compare[df_compare['_merge'] == 'left_only'][unique_cols[i]])
            print('\n\nIn mine, not in solution:\n')
            print(df_compare[df_compare['_merge'] == 'right_only'][unique_cols[i]]) 
            errors += 1

        # for the records that matched, check for mismatched values
        for c in [c for c in df_sol.columns if c not in unique_cols[i]]:
            if 'float' in df_compare[f'{c}_sol'].dtype.name:
                df_compare[f'{c}_sol'] = df_compare[f'{c}_sol'].round(round_dec)
                df_compare[f'{c}_mine'] = df_compare[f'{c}_mine'].round(round_dec)
                
            unmatched = df_compare[(df_compare['_merge']=='both')
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])
                                   & ((df_compare[f'{c}_sol'].notna()) 
                                      | (df_compare[f'{c}_mine'].notna()))]

            if len(unmatched) > 0:
                print(f'\n\n*** Values do not match: {c} ***\n')
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                errors += 1
        
        if errors == 0:
            print('Values match')

    print('\n')  
