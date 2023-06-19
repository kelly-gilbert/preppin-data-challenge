# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 05 - DSB Ranking (Polars)
https://preppindata.blogspot.com/2023/02/2023-week-5-dsb-ranking.html

- Input data
- Create the bank code by splitting out off the letters from the Transaction code, call this field 'Bank'
- Change transaction date to the just be the month of the transaction
- Total up the transaction values so you have one row for each bank and month combination
- Rank each bank for their value of transactions each month against the other banks. 1st is the 
  highest value of transactions, 3rd the lowest. 
- Without losing all of the other data fields, find:
  - The average rank a bank has across all of the months, call this field 'Avg Rank per Bank'
  - The average transaction value per rank, call this field 'Avg Transaction Value per Rank'
- Output the data

Author: Kelly Gilbert
Created: 2023-06-19
Requirements:
  - input dataset:
      - PD 2023 Wk 1 Input.csv
  - output dataset (for results check only):
      - PD 2023 Wk 5 Output.csv 
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

df = ( pl.read_csv(r'.\inputs\PD 2023 Wk 1 Input.csv', 
                   try_parse_dates=True)
         .with_columns(
             [pl.col('Transaction Code').str.split('-').list.first().alias('Bank'),
              pl.col('Transaction Date').dt.strftime('%B')]
         )
         
         # sum value by bank and month
         .groupby(['Transaction Date', 'Bank'])
         .agg(pl.col('Value').sum())
         
         # rank
         .with_columns(pl.col('Value').rank(method='min', descending=True)
                         .over('Transaction Date')
                         .alias('Bank Rank per Month')
         )
         .with_columns(pl.col('Value').mean()
                         .over('Bank Rank per Month')
                         .alias('Avg Transaction Value per Rank'),
                       pl.col('Bank Rank per Month').mean()
                         .over('Bank')
                         .alias('Avg Rank per Bank'))
     )
         
         
#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.write_csv(r'.\outputs\output-2023-05.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2023 Wk 5 Output.csv']
my_files = [r'.\outputs\output-2023-05.csv']
unique_cols = [['Bank', 'Transaction Date']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
