# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 07 - Flagging Fraudulent Suspicions (polars)
https://preppindata.blogspot.com/2023/02/2023-week-7-flagging-fraudulent.html

- Input the data
- For the Transaction Path table:
  - Make sure field naming convention matches the other tables
    - i.e. instead of Account_From it should be Account From
- For the Account Information table:
  - Make sure there are no null values in the Account Holder ID
  - Ensure there is one row per Account Holder ID
    - Joint accounts will have 2 Account Holders, we want a row for each of them
- For the Account Holders table:
  - Make sure the phone numbers start with 07
- Bring the tables together
- Filter out cancelled transactions 
- Filter to transactions greater than £1,000 in value 
- Filter out Platinum accounts
- Output the data

Author: Kelly Gilbert
Created: 2023-06-20
Requirements:
  - input dataset:
      - Account Holders.csv
      - Account Information.csv
      - Transaction Detail.csv
      - Transaction Path.csv
  - output dataset (for results check only):
      - Flagged transactions.csv
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# transaction path
df_txnpath = ( pl.read_csv(r'.\inputs\Transaction Path.csv')
                 .rename({ 'Account_To' : 'Account To',
                           'Account_From' : 'Account Number'}) 
             )


# account info - split joint account holders into rows
df_acctinfo = ( pl.read_csv(r'.\inputs\Account Information.csv',
                            try_parse_dates=True)
                  .filter( (pl.col('Account Holder ID').is_not_null()) 
                           & (pl.col('Account Type') != 'Platinum') )
                  .with_columns( 
                      pl.col('Account Holder ID').str.split(', ')
                  )
                  .explode('Account Holder ID')
                  .with_columns( 
                      pl.col('Account Holder ID').cast(pl.Int64))
              )
    

# account holders
df_accthold = ( pl.read_csv(r'.\inputs\Account Holders.csv',
                            try_parse_dates=True)
                  .with_columns(
                      pl.col('Contact Number')
                        .cast(pl.Utf8)
                        .str.replace('^7', '07')
                  )
              )


# transaction detail
df_txndtl = ( pl.read_csv(r'.\inputs\Transaction Detail.csv',
                          try_parse_dates=True)
                .filter(pl.col('Cancelled?').eq('N') & pl.col('Value').ge(1000))
            )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

out_cols = ['Transaction ID', 'Account To', 'Transaction Date', 'Value', 'Name',
                       'Date of Birth', 'Contact Number', 'First Line of Address',
                       'Account Number', 'Account Type', 'Balance Date', 'Balance']

# join the tables together
df_out = ( df_txndtl
              .join(df_txnpath,
                    on='Transaction ID',
                    how='inner')
              .join(df_acctinfo,
                    on='Account Number',
                    how='inner')
              .join(df_accthold,
                    on='Account Holder ID',
                    how='inner')
              .select(pl.col(out_cols))
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.write_csv(r'.\outputs\output-2023-07.csv', 
                 date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Flagged transactions.csv']
my_files = [r'.\outputs\output-2023-07.csv']
unique_cols = [['Transaction ID', 'Account To', 'Account Number', 'Name']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
