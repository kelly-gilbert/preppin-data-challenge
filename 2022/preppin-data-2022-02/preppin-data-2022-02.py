# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 2 The Prep School - Birthday Cakes
https://preppindata.blogspot.com/2022/01/2022-week-2-prep-school-birthday-cakes.html

- Input data
    - Removing any unnecessary fields (parental fields) will make this challenge easier to see what 
      is happening at each step
- Format the pupil's name in First Name Last Name format (ie Carl Allchin)
- Create the date for the pupil's birthday in calendar year 2022 (not academic year)
- Work out what day of the week the pupil's birthday falls on
- Remember if the birthday falls on a Saturday or Sunday, we need to change the weekday to Friday
- Work out what month the pupil's birthday falls within
- Count how many birthdays there are on each weekday in each month
- Output the data

Author: Kelly Gilbert
Created: 2022-01-12
Requirements:
  - input dataset:
      - PD 2022 Wk 1 Input - Input.csv
  - output dataset (for results check only):
      - PD 2022 Wk 2 Output.csv
"""

import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\PD 2022 Wk 1 Input - Input.csv', parse_dates=['Date of Birth'],
                 usecols=['id', 'pupil first name', 'pupil last name', 'Date of Birth'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# format the pupil's name in First Name Last Name format (ie Carl Allchin)
df['Pupil Name'] = df['pupil first name'] + ' ' + df['pupil last name']


# create the date for the pupil's birthday in calendar year 2022 (not academic year)
df['This Year\'s Birthday'] = df['Date of Birth'].apply(lambda x: x.replace(year=datetime.now().year))


# birthday weekday and month
df['Cake Needed On'] = df['This Year\'s Birthday'].dt.day_name()\
                                                  .replace({'Saturday':'Friday', 'Sunday':'Friday'})
df['Month'] = df['This Year\'s Birthday'].dt.month_name()


# count how many birthdays there are on each weekday in each month
df['BDs per Weekday and Month'] = df.groupby(['Cake Needed On', 'Month'])['id'].transform('size')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

columns = ['Pupil Name', 'Date of Birth', 'This Year\'s Birthday', 'Month', 'Cake Needed On', 
           'BDs per Weekday and Month']
df.to_csv(r'.\outputs\output-2021-02.csv', index=False, columns=columns, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2022 Wk 2 Output.csv']
my_files = ['output-2021-02.csv']
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


#---------------------------------------------------------------------------------------------------
# profiling
#---------------------------------------------------------------------------------------------------

from pandas import concat
from pandas import offsets
import timeit
from pandas import to_datetime

df_big = read_csv(r'.\inputs\PD 2022 Wk 1 Input - Input.csv', parse_dates=['Date of Birth'],
              usecols=['id', 'pupil first name', 'pupil last name', 'Date of Birth'])

df_big = concat([df_big]*1000)


# using replace
%timeit -n 1 -r 100 df_big['This Year\'s Birthday'] = df_big['Date of Birth'].apply(lambda x: x.replace(year=datetime.now().year))

# using offsets
%timeit -n 1 -r 100 df_big['This Year\'s Birthday'] = df_big['Date of Birth'] + offsets.DateOffset(year=2022)

# using string formatting
%timeit -n 1 -r 100 df_big['This Year\'s Birthday'] = to_datetime('2022-' + df_big['Date of Birth'].dt.strftime('%m-%d'))
