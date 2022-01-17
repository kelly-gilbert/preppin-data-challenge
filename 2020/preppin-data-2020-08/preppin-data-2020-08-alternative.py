# -*- coding: utf-8 -*-
"""
Preppin' Data 2020: Week 8
https://preppindata.blogspot.com/2020/02/2020-week-8.html

- Input data (*** Updated on 20th Feb 9pm GMT ***)
- Pull all the Week worksheets together
- Form weekly sales volume and value figures per product
- Prepare the data in the Profit table for comparison against the actual volumes and values
- Join the tables but only bring back those that have exceeded their Profit Min points for both 
  Value and Volume
- Prepare the Budget Volumes and Values for comparison against the actual volumes and values
- Join the tables but only return those that haven't reached the budget expected for either
  Value or Volume
- Prepare the outputs
- Output the data

Author: Kelly Gilbert
Created: 2020-MM-DD
Requirements:
  - pandas version 1.3.0+ (previous versions dropped the headerless columns on the budget sheet)
  - input dataset:
      - PD 2020 Wk 8 Input Not Random.xlsx
  - output datasets (for results check only):
      - PD 2020 Wk 8 Output Budget Missed.csv
      - PD 2020 Wk 8 Output Profit Expectations Exceeded.csv
      
"""


from datetime import datetime
from numpy import sum
import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\PD 2020 Wk 8 Input Not Random.xlsx') as xl:
    
    # import the weekly sheets, then group by type and week
    renames = {'Volume' : 'Sales Volume', 'Value' : 'Sales Value'}
    df_weekly = pd.concat([pd.read_excel(xl, s)\
                             .assign(Week=int(s.replace('Week ', '')))\
                             .rename(columns=renames)
                           for s in xl.sheet_names if 'Week' in s])\
                  .assign(Type=lambda df_x: df_x['Type'].str.lower())\
                  .groupby(['Week', 'Type'], as_index=False)[['Sales Volume', 'Sales Value']].sum()
    
    # import the budget sheet    
    df_budget_in = pd.read_excel(xl, 'Budget', skiprows=2)\
                     .dropna(how='all', axis=1)\
                     .rename(str.strip, axis=1)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# dynamically split the Budget sheet into profit and budget tables
header_row = df_budget_in[df_budget_in['Week']=='Type'].index[0]

df_profit = df_budget_in.iloc[0:header_row]\
                        .dropna(how='all', axis=1)\
                        .dropna(how='all', axis=0)\
                        .assign(Year=lambda df_x: df_x['Week'].str[0:4],
                                Week=lambda df_x: df_x['Week'].str.extract('.*\_(\d+)').astype(int),
                                Type=lambda df_x: df_x['Type'].str.lower())


# extract the budget table and reshape it with Measures in columns and week ranges in rows
df_budget = df_budget_in.iloc[header_row + 1:]\
                        .set_axis([c.strftime('%d-%m') if isinstance(c, datetime) else c 
                                  for c in df_budget_in.iloc[header_row]], axis=1)\
                        .melt(id_vars=['Type', 'Measure'], var_name='Week')\
                        .assign(Type=lambda df_x: df_x['Type'].str.replace('[\d_]', '', regex=True).str.lower(),
                                Start_Week=lambda df_x: df_x['Week'].str[0:2].astype(int),
                                End_Week=lambda df_x: df_x['Week'].str[3:].astype(int),
                                value=lambda df_x: df_x['value'].astype(float))\
                        .pivot_table(index=['Type', 'Start_Week', 'End_Week', 'Week'], values='value', 
                                     columns=['Measure'], aggfunc=sum)\
                        .reset_index()

                        
# create a row for each week in the budget table                        
df_budget = df_budget.assign(Week=[list(range(i, j+1)) 
                                    for i, j in df_budget[['Start_Week', 'End_Week']].values])\
                     .explode('Week')

# I could have used merge_asof to join on the Start Week (rather than exploding the DataFrame to 
#    include one row per week). However, I wanted to handle products that had no sales for a week.


# Output 1: week/type exceeded min for both volume and value
df_profit_out = df_profit.merge(df_weekly, on=['Week', 'Type'], how='left')
df_profit_out = df_profit_out.loc[(df_profit_out['Sales Volume'] > df_profit_out['Profit Min Sales Volume'])
                                  & (df_profit_out['Sales Value'] > df_profit_out['Profit Min Sales Value'])]


# Output 2: week/type did not reach budget for either volume or value
df_budget_out = df_budget.merge(df_weekly, on=['Week', 'Type'], how='left')
df_budget_out = df_budget_out.loc[(df_budget_out['Sales Volume'] < df_budget_out['Budget Volume'])
                                  | (df_budget_out['Sales Value'] < df_budget_out['Budget Value'])]\
                             .rename(columns=lambda x: x.replace('_', ' '))


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_profit_out.to_csv(r'.\outputs\output-2020-08-profit.csv', index=False,
                     columns=['Sales Volume', 'Sales Value', 'Week', 'Type', 'Profit Min Sales Volume',
                              'Profit Min Sales Value'])
df_budget_out.to_csv(r'.\outputs\output-2020-08-budget.csv', index=False,
                     columns=['Type', 'Sales Volume', 'Budget Volume', 'Sales Value', 'Budget Value', 
                              'Week', 'Start Week', 'End Week'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2020 Wk 8 Output Budget Missed.csv', 
                  'PD 2020 Wk 8 Output Profit Expectations Exceeded.csv']
my_files = ['output-2020-08-budget.csv', 'output-2020-08-profit.csv']
unique_cols = ['Week', 'Type']
col_order_matters = True
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
