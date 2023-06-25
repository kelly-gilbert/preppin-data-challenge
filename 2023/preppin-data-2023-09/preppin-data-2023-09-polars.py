# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 09 - Customer Bank Statements (polars)
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


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input transaction path and melt to/from into rows
df_txnpath = ( pl.scan_csv(r'.\inputs\Transaction Path.csv')
                 .select(
                     pl.all().map_alias(lambda c: c.replace('_', ' '))
                 )
                 .melt(id_vars='Transaction ID',
                       variable_name='Direction',
                       value_name='Account Number') 

             )


# input transaction detail and join to path data
df_txndtl = ( pl.scan_csv(r'.\inputs\Transaction Detail.csv', 
                          try_parse_dates=True)
                .filter(pl.col('Cancelled?') == 'N')
                .join(df_txnpath,
                      on='Transaction ID',
                      how='inner')
                .with_columns(
                    pl.when(pl.col('Direction')=='Account From')
                      .then(-pl.col('Value'))
                      .otherwise(pl.col('Value'))
                      .alias('Transaction Value')
                )
                .select(
                    pl.col(['Account Number', 'Transaction Date', 'Transaction Value'])
                )
                .rename({'Transaction Date' : 'Balance Date'})
            )
                
                
# account info
df_acctinfo = ( pl.scan_csv(r'.\inputs\Account Information.csv',
                            try_parse_dates=True)
                  .select(
                      pl.col(['Account Number', 'Balance Date', 'Balance'])
                  )
                  .rename({'Balance' : 'Transaction Value'})
              )
                  

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# concat opening balances to transactions transactions and calc running balance
df_out = ( pl.concat(
               [df_acctinfo, df_txndtl]      
           )     
           .sort(by=['Account Number', 'Balance Date', 'Transaction Value'],
                 descending=[False, False, True])
           
           # calculate running balance
           .with_columns(
               pl.col('Transaction Value').cumsum()
                 .over(['Account Number'])
                 .alias('Balance')               
           )
           
           # set value to none if it is the opening balance
           .with_columns( 
               pl.when(pl.col('Balance Date')==pl.col('Balance Date').min())
                 .then(None)
                 .otherwise(pl.col('Transaction Value'))
                 .alias('Transaction Value')
           )
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Account Number', 'Balance Date', 'Transaction Value', 'Balance']

( df_out
     .select(
         pl.col(out_cols) 
     )
     .collect()
     .write_csv(r'.\outputs\output-2023-09.csv', 
                date_format='%d/%m/%Y')
)


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
