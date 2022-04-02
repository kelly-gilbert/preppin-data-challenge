# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 13 - Pareto Parameters
https://preppindata.blogspot.com/2022/03/2022-week-13-pareto-parameters.html

- Input the data
- Aggregate the data to the total sales for each customer
- Calculate the percent of total sales each customer represents
- Calculate the running total of sales across customers
    - Order by the percent of total in a descending order
  - Round to 2 decimal places
- Create a parameter that will allow the user to decide the percentage of sales they wish to filter to
- Output the data, including the parameter in the output name
- Create a second output that describes the result in plain English
  - e.g. 50% of Customers account for 80% of Sales 

Author: Kelly Gilbert
Created: 2022-03-31
Requirements:
  - input dataset:
      - Pareto Input.csv
  - output dataset (for results check only):
      - Pareto in words 80%.csv
      - Pareto Output 80%.csv
"""


import pandas as pd
import sys


#---------------------------------------------------------------------------------------------------
# get the user input
#---------------------------------------------------------------------------------------------------

FILTER_PCT = input('Enter the % of sales threshold (enter a number between 0 and 100):')


try:
    FILTER_PCT = float(FILTER_PCT)
except:
    print('Please enter a valid number.')
    sys.exit()
    
if FILTER_PCT < 0 or FILTER_PCT > 100:
    print('Please enter a number between 0 and 100.')
    sys.exit()


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_orders = pd.read_csv(r'.\inputs\Pareto Input.csv')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# aggregate the data to the total sales for each customer, add % of sales and cuml % of sales
df = df_orders.groupby(['Customer ID', 'First Name', 'Surname'], as_index=False)['Sales'].sum()\
              .sort_values(by='Sales', ascending=False)\
              .reset_index(drop=True)\
              .assign(Pct_of_Total=lambda df_x: round(df_x['Sales'] / df_x['Sales'].sum() * 100, 9),
                      Total_Customers=lambda df_x: len(df_x.index))\
              .assign(Running_Pct_Total_Sales=lambda df_x: df_x['Pct_of_Total'].cumsum().round(2))    


# describe the result in plain English
filter_rows = df[df['Running_Pct_Total_Sales'] <= FILTER_PCT]['Customer ID'].count()
outcome = f'{filter_rows / len(df.index):.0%} of Customers account for {FILTER_PCT}% of Sales'


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Total Customers', 'Running % Total Sales', '% of Total', 'Customer ID', 'First Name', 
            'Surname', 'Sales']

# write out the table
df.iloc[0:filter_rows].rename(columns=lambda x: x.replace('_', ' ').replace('Pct', '%'))\
  .to_csv(f'.\\outputs\\output-2022-13-Pareto Output {FILTER_PCT}%.csv', index=False, 
          columns=out_cols, encoding='utf-8')


# write out the words
with open(f'.\\outputs\\output-2022-13-Pareto in words {FILTER_PCT}%.csv', mode='w') as f:
    f.write('Outcome\n' + outcome)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Pareto in words 80%.csv', 'Pareto Output 80%.csv']
my_files = ['output-2022-13-Pareto in words 80%.csv', 'output-2022-13-Pareto Output 80%.csv']
unique_cols = [['Outcome'], ['Customer ID']]
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
