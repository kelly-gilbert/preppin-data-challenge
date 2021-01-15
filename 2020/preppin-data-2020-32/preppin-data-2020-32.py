# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-32
https://preppindata.blogspot.com/2020/08/2020-week-32.html
 
Copying down data

- Leave no nulls in the table
- No manual entry of data points though!! 
- We want solutions that would work if this table got bigger and we added 
  another manager for different stores. 
- Output the data

Author: Kelly Gilbert
Created: 2020-08-06

Requirements: input dataset
  - Copy Down Data Challenge.xlsx
  - pandas version 0.19.0 or higher
"""


from pandas import merge_asof, read_csv, read_excel


#------------------------------------------------------------------------------
# Method 1: ffill
#------------------------------------------------------------------------------

# import and fill the data
df = read_excel('.\\inputs\\Copy Down Data Challenge.xlsx')
df.ffill(inplace=True)

# output the data
df.rename(columns={ 'Sales Target ' : 'Sales Target' }, inplace=True)
df.to_csv('.\\outputs\\output-2020-32_method1.csv', index=False, 
          columns=['Store Manager', 'Store', 'Sales Target'])



#------------------------------------------------------------------------------
# Method 2: merge_asof (non-equijoin)
#------------------------------------------------------------------------------

# import and fill the data
df = read_excel('.\\inputs\\Copy Down Data Challenge.xlsx')

df_managers = df[['Row ID', 'Store Manager']][df['Store Manager'].notna()]
merge_asof(df, df_managers, on='Row ID', direction='backward')


# output the data
df.rename(columns={ 'Sales Target ' : 'Sales Target',
                    'Store Manager_y' : 'Store Manager' }, inplace=True)
df.to_csv('.\\outputs\\output-2020-32_method2.csv', index=False, 
          columns=['Store Manager', 'Store', 'Sales Target'])



#------------------------------------------------------------------------------
# check results
#------------------------------------------------------------------------------

df_sol = read_csv('.\\outputs\\PD 2020 Week 32 Output.csv')
df_mine = read_csv('.\\outputs\\output-2020-32_method2.csv')

df_check = df_sol.merge(df_mine, suffixes=['_sol','_mine'], how='outer', 
                        on=['Store'])


# columns match?
if list(df_sol.columns) == list(df_mine.columns):
    print('\nColumns match')
else:
    print('\nColumns do not match:')
    print('\nSolution columns: ' + str(df_sol.columns))
    print('\nMy columns: ' + str(df_mine.columns))

# missing from mine?
print('\nIn solution, not in mine:')
unmatched = df_check[df_check['Sales Target_sol'].isna()]
if len(unmatched)==0:
    print('None')
else:
    print(unmatched)

# extra records in mine?
print('\nIn mine, not in solution:')
unmatched = df_check[df_check['Sales Target_mine'].isna()]
if len(unmatched)==0:
    print('None')
else:
    print(unmatched)

# values do not match?
print('\nStore Manager value does not match:')
unmatched = df_check[df_check['Store Manager_sol'] != df_check['Store Manager_mine']]
if len(unmatched)==0:
    print('None')
else:
    print(unmatched)
