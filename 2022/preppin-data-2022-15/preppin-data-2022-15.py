# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 15 - Property Management
https://preppindata.blogspot.com/2022/04/2022-week-15-property-management.html

- Input the Rental Contracts data
- Work out the length of each contract in months 
- Work out the number of months until each contract expires (imagine today is 13th April 2022)
- Input the Office Space Prices data and join it to the contracts table
- Remove duplicated fields
- Create a row for each month that a rental contract will be live
- Retain the details for each of the contracts in the new rows
- Edit 14/04/2022: Be careful at this point that the number of rows for each Office ID is equal to the Contract length
- Calculate the cumulative monthly cost of each office space contract
- Remember we only have one contract per company
- This will create our first output
- Create a table that details total rent paid for completed years across all contracts and year to 
  date figures for the current year, which would update as time goes on
- This will create our second output


Author: Kelly Gilbert
Created: 2022-04-14

Requirements:
  - input datasets:
      - Office Space Prices.xlsx
      - Rental Contracts.xlsx
  - output datasets (for results check only):
      - 2022W15 Output 1.csv
      - 2022W15 Output2.csv
  - output_check module (for results check only)
  
"""


from datetime import datetime
import numpy as np
import pandas as pd
import output_check  # custom module for comparing output to the solution file


CURRENT_DATE = pd.to_datetime('2022-04-13')


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_p = pd.read_excel(r'.\inputs\Office Space Prices.xlsx')
df_c = pd.read_excel(r'.\inputs\Rental Contracts.xlsx')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df_c['Current Date'] = CURRENT_DATE

# work out the length of each contract in months 
df_c['Contract Length'] = df_c['Contract End'].dt.to_period('M').view('int64') \
                          - df_c['Contract Start'].dt.to_period('M').view('int64')


# work out the number of months until each contract expires (imagine today is 13th April 2022)
df_c['Months Until Expiry'] = df_c['Contract End'].dt.to_period('M').view('int64') \
                              - df_c['Current Date'].dt.to_period('M').view('int64') 


# join to the pricing table and create one row per month begin date                              
df = df_c.merge(df_p, on=['City', 'Office Size'], how='left')\
         .assign(Month_Divider=\
                 lambda df_x: [pd.date_range(s, e, freq=pd.DateOffset(months=1)).union([e]) 
                               for s, e in zip(df_x['Contract Start'], df_x['Contract End'])])\
         .explode('Month_Divider')\
         .rename(columns=lambda x: x.replace('_', ' '))
         

# calculate the cumulative monthly cost of each office space contract
df['Cumulative Monthly Cost'] = df.groupby('ID')['Rent per Month'].transform('cumsum')
         
         
# Create a table that details total rent paid for completed years across all contracts and year to
# date figures for the current year, which would update as time goes on
df2 = df.assign(Year=lambda df_x: df_x['Month Divider'].dt.year,
                value=lambda df_x: np.where(df_x['Month Divider'] < CURRENT_DATE, 
                                            df_x['Rent per Month'], np.NaN))\
        .groupby('Year', as_index=False)['value'].sum(min_count = 1)\
        .rename(columns={'value' : 'EoY and Current'})


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# output 1
out_cols1 = ['Cumulative Monthly Cost', 'ID', 'Country', 'City', 'Address', 'Company', 'Office Size', 
             'Contract Start', 'Contract End', 'Contract Length', 'Months Until Expiry', 'People', 
             'Per Person', 'Rent per Month', 'Month Divider']
df.to_csv(r'.\outputs\output-2022-15-1.csv', index=False, columns=out_cols1, date_format='%d/%m/%Y')


# output 2
df2.to_csv(r'.\outputs\output-2022-15-2.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W15 Output 1.csv', r'.\outputs\2022W15 Output2.csv']
my_files = [r'.\outputs\output-2022-15-1.csv', r'.\outputs\output-2022-15-2.csv']
unique_cols = [['ID', 'Month Divider'], ['Year']]
col_order_matters = True
round_dec = 8

output_check.output_check(solution_files, my_files, unique_cols, col_order_matters = False)




#---------------------------------------------------------------------------------------------------
# examples of ways to calculate month diff
#---------------------------------------------------------------------------------------------------

# create test data 
test = pd.DataFrame({'date1' : ['2021-05-01', '2021-01-05', '2021-01-05', '2021-01-05', '2019-12-01'], 
                     'date2' : ['2022-04-30', '2021-05-03', '2021-05-05', '2021-05-10', '2020-03-01'],
                     'want' : [12, 3, 4, 4, 3]})\
         .assign(date1=lambda df_x: pd.to_datetime(df_x.date1),
                 date2=lambda df_x: pd.to_datetime(df_x.date2))
         
# method 1: timedelta -- this counts fractional months
import numpy as np
test['np_timedelta'] = ((test.date2 - test.date1) / np.timedelta64(1, 'M') ) 
test

# method 2: timedelta + 1 day
test['np_timedelta2'] = ((test.date2 - test.date1 + np.timedelta64(1, 'D')) / np.timedelta64(1, 'M') ) 
test

# method 3: to_period -- counts the number of month ends included in the range
#    frequency string M = month end; frequency string MS = month start
%%timeit 
test['to_period'] = test.date2.dt.to_period('M').view(dtype='int64') \
                    - test.date1.dt.to_period('M').view(dtype='int64') + 1

# method 4 year/month numbers
%%timeit 
test['yr_mo'] = (test.date2.dt.year - test.date1.dt.year) * 12 \
                + (test.date2.dt.month - test.date1.dt.month) + 1

