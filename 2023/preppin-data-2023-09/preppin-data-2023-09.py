# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 09 - Customer Bank Statements
https://preppindata.blogspot.com/2023/03/2023-week-9-customer-bank-statements.html

- Input the data
- For the Transaction Path table:
  - Make sure field naming convention matches the other tables
    - i.e. instead of Account_From it should be Account From
- Filter out the cancelled transactions
- Split the flow into incoming and outgoing transactions 
- Bring the data together with the Balance as of 31st Jan 
- Work out the order that transactions occur for each account
  - Hint: where multiple transactions happen on the same day, assume the highest value transactions
   happen first
- Use a running sum to calculate the Balance for each account on each day (hint)
- The Transaction Value should be null for 31st Jan, as this is the starting balance
- Output the data

Author: Kelly Gilbert
Created: 2023-06-24
Requirements:
  - input dataset:
      - Account Holders.csv
      - Account Information.csv
      - Transaction Detail.csv
      - Transaction Path.csv
  - output dataset (for results check only):
      - Account Statements.csv 
"""


from numpy import NaN, where
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input transaction path and melt to/from into rows
df_txnpath = ( pd.read_csv(r'.\inputs\Transaction Path.csv')
                 .rename(columns=lambda c: c.replace('_', ' '))
                 .melt(id_vars='Transaction ID',
                       var_name='Direction',
                       value_name='Account Number') )


# input transaction detail and join to path data
df_txndtl = ( pd.read_csv(r'.\inputs\Transaction Detail.csv', 
                          parse_dates=['Transaction Date'], dayfirst=True)
                .query("`Cancelled?` == 'N'")
                .merge(df_txnpath,
                       on='Transaction ID',
                       how='inner')
                .assign(Value = lambda df_x: where(df_x['Direction']=='Account From',
                                                   -df_x['Value'],
                                                   df_x['Value']))
                .rename(columns={'Value' : 'Transaction Value',
                                 'Transaction Date' : 'Balance Date'}) )
                
                
# account info
df_acctinfo = ( pd.read_csv(r'.\inputs\Account Information.csv',
                            parse_dates=['Balance Date'], dayfirst=True,
                            usecols=['Account Number', 'Balance Date', 'Balance'])
                  .rename(columns={'Balance' : 'Transaction Value'}) )
                  

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# append the transactions to the opening balances, sort by acct/date/amount
df_out = ( pd.concat([df_acctinfo, 
                      df_txndtl[['Account Number', 'Balance Date', 'Transaction Value']]], 
                     ignore_index=True)
             .sort_values(['Account Number', 'Balance Date', 'Transaction Value'],
                          ascending=[True, True, False]) )


# calculate the running balance
df_out['Balance'] = ( df_out.groupby('Account Number', as_index=False)
                            ['Transaction Value'].cumsum() )


# null the transaction value for opening balances
df_out['Transaction Value'] = where((df_out['Balance Date']==df_acctinfo['Balance Date'].min())
                                    & (df_out['Transaction Value']==df_out['Balance']),
                                    NaN,
                                    df_out['Transaction Value'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2023-09.csv', 
              index=False,
              columns=['Account Number', 'Balance Date', 'Transaction Value', 'Balance'],
              date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Account Statements.csv']
my_files = [r'.\outputs\output-2023-09.csv']
unique_cols = [['Account Number', 'Balance Date', 'Transaction Value']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
