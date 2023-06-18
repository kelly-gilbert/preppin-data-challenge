# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 01 - The Data Source Bank (Polars version)
https://preppindata.blogspot.com/2023/01/2023-week-1-data-source-bank.html

- Input the data
- Split the Transaction Code to extract the letters at the start of the transaction code. These 
  identify the bank who processes the transaction
  - Rename the new field with the Bank code 'Bank'. 
- Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values. 
- Change the date to be the day of the week
- Different levels of detail are required in the outputs. You will need to sum up the values of the 
  transactions in three ways:
  - 1. Total Values of Transactions by each bank
  - 2. Total Values by Bank, Day of the Week and Type of Transaction (Online or In-Person)
  - 3. Total Values by Bank and Customer Code
- Output each data file

Author: Kelly Gilbert
Created: 2023-04-14
Requirements:
  - input dataset:
      - PD 2023 Wk 1 Input.csv
  - output dataset (for results check only):
      - PD 2023 Wk 1 Bank Totals.csv
      - PD 2023 Wk 1 Bank Totals by Transaction Type.csv
      - PD 2023 Wk 1 Bank Transactions by Customer.csv
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data and parse the fields
#---------------------------------------------------------------------------------------------------

LOCATION_RENAMES = { 1 : 'Online',
                     2 : 'In-Person' }


df = ( pl.read_csv(r'.\inputs\PD 2023 Wk 1 Input.csv', 
                   try_parse_dates=True)
         .with_columns(
             [ pl.col('Transaction Date').dt.strftime(format='%A'),
               pl.col('Transaction Code').str.split('-').list.first().alias('Bank'),
               pl.col('Online or In-Person').map_dict(LOCATION_RENAMES, 
                                                      default=pl.col('Online or In-Person'))
             ]
         )
      )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# output 1 - Total Values of Transactions by each bank
( df.groupby('Bank')
    .agg(pl.col('Value').sum())    
    .write_csv(r'.\outputs\output-2023-01-part1.csv') )


# output 2 - Total Values by Bank, Day of the Week and Type of Transaction (Online or In-Person)
( df.groupby(['Bank', 'Online or In-Person', 'Transaction Date'])
    .agg(pl.col('Value').sum())
    .write_csv(r'.\outputs\output-2023-01-part2.csv') ) 


# output 3 - Total Values by Bank and Customer Code
( df.groupby(['Bank', 'Customer Code'])
    .agg(pl.col('Value').sum())
    .write_csv(r'.\outputs\output-2023-01-part3.csv') ) 


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2023 Wk 1 Bank Totals.csv',
                  r'.\outputs\PD 2023 Wk 1 Bank Totals by Transaction Type.csv',
                  r'.\outputs\PD 2023 Wk 1 Bank Transactions by Customer.csv']
my_files = [r'.\outputs\output-2023-01-part1.csv', 
            r'.\outputs\output-2023-01-part2.csv', 
            r'.\outputs\output-2023-01-part3.csv']
unique_cols = [['Bank'], 
               ['Bank', 'Online or In-Person', 'Transaction Date'],
               ['Bank', 'Customer Code']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
