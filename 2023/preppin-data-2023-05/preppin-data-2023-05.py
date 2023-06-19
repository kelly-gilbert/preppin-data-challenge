# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 05 - DSB Ranking
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


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data and group by bank/month
#---------------------------------------------------------------------------------------------------

df = ( pd.read_csv(r'.\inputs\PD 2023 Wk 1 Input.csv', 
                   parse_dates=['Transaction Date'], 
                   dayfirst=True)
         .assign(Bank = lambda df_x: df_x['Transaction Code'].str.split('-', n=1, expand=True)[0],
                 Month = lambda df_x: df_x['Transaction Date'].dt.strftime('%B'))
         .groupby(['Month', 'Bank'], as_index=False)['Value'].sum()
         .rename(columns={'Month' : 'Transaction Date'})
     )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# rank the banks within each month
df['Bank Rank per Month'] = df.groupby('Transaction Date')['Value'].rank(ascending=False).astype(int)

# find averages
df['Avg Transaction Value per Rank'] = df.groupby('Bank Rank per Month')['Value'].transform('mean')
df['Avg Rank per Bank'] = df.groupby('Bank')['Bank Rank per Month'].transform('mean')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2023-05.csv', index=False)


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
