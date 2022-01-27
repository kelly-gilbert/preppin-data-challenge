# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 4 The Prep School - Travel Plans
https://preppindata.blogspot.com/2022/01/2022-week-4-prep-school-travel-plans.html

- Input the data sets
- Join the data sets together based on their common field
- Remove any fields you don't need for the challenge
- Change the weekdays from separate columns to one column of weekdays and one of the pupil's travel choice
- Group the travel choices together to remove spelling mistakes
- Create a Sustainable (non-motorised) vs Non-Sustainable (motorised) data field 
- Scooters are the child type rather than the motorised type
- Total up the number of pupil's travelling by each method of travel 
- Work out the % of trips taken by each method of travel each day
- Round to 2 decimal places
- Output the data

Author: Kelly Gilbert
Created: 2022--01-26
Requirements:
  - input dataset:
      - PD 2022 Wk 1 Input - Input.csv
      - PD 2021 WK 1 to 4 ideas - Preferences of Travel.csv
  - output dataset (for results check only):
      - PD 2022 Wk 4 Output.csv
"""


import numpy as np
import pandas as pd


#---------------------------------------------------------------------------------------------------
# setup
#---------------------------------------------------------------------------------------------------

travel_method_renames = {'Bycycle' : 'Bicycle',
                         'Carr' : 'Car',
                         'Helicopeter' : 'Helicopter',
                         'Scootr' : 'Scooter', 'Scoter' : 'Scooter',
                         'WAlk' : 'Walk', 'Waalk' : 'Walk', 'Wallk' : 'Walk', 'Walkk' : 'Walk'}

sustainable_methods = ['Bicycle', "Dad's Shoulders", 'Hopped', 'Jumped', "Mum's Shoulders", 
                       'Scooter', 'Skipped', 'Walk']


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\PD 2021 WK 1 to 4 ideas - Preferences of Travel.csv')
df_students = pd.read_csv(r'.\inputs\PD 2022 Wk 1 Input - Input.csv', usecols=['id'])\
                .rename(columns={'id' : 'Student ID'})


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# join the data sets together based on their common field, then melt weekdays into rows
# [KLG: the join doesn't seem necessary for the result. I think it's just for practice!]
df = df.merge(df_students, on='Student ID', how='inner')\
       .melt(id_vars='Student ID', var_name='Weekday', value_name='Method of Travel')
           
       
# clean Method of Travel and add sustainable flag
df['Method of Travel'] = df['Method of Travel'].replace(travel_method_renames)
df['Sustainable?']  = np.where(df['Method of Travel'].isin(sustainable_methods),
                              'Sustainable', 'Non-Sustainable')


# sum by Method and Weekday, calculate the % of daily trips
df_out = df.groupby(['Sustainable?', 'Method of Travel', 'Weekday'], as_index=False)\
           .agg(Number_of_Trips=('Student ID', 'count'))\
           .assign(Trips_per_day = lambda df_x: df_x.groupby('Weekday')['Number_of_Trips'].transform('sum'),
                   Pct_of_trips_per_day = lambda df_x: (df_x['Number_of_Trips'] 
                                                        / df_x['Trips_per_day']).round(2))\
           .rename(columns=lambda c: c.replace('_', ' ').replace('Pct', '%'))


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-04.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2022 Wk 4 Output.csv']
my_files = ['output-2022-04.csv']
unique_cols = [['Sustainable?', 'Method of Travel', 'Weekday']]
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
            print('*** Missing or extra records ***\n')
            print('In solution, not in mine:\n')
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
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]
            if len(unmatched) > 0:
                print(f'*** Values do not match: {c} ***\n')
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                errors += 1

        if errors == 0:
            print('Values match')

    print('\n')  
