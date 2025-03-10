# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 07 - Flagging Fraudulent Suspicions
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


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# transaction path
df_txnpath = ( pd.read_csv(r'.\inputs\Transaction Path.csv')
                 .rename(columns=lambda c: c.replace('_', ' ')) )


# account info - split joint account holders into rows
df_acctinfo = ( pd.read_csv(r'.\inputs\Account Information.csv',
                            parse_dates=['Balance Date'],
                            dayfirst=True)
                  .query("`Account Holder ID` == `Account Holder ID` & `Account Type` != 'Platinum'")
                  .assign(Account_Holder_ID=lambda df_x: df_x['Account Holder ID']
                                                             .str.replace(' ', '')
                                                             .str.split(','))
                  .explode('Account_Holder_ID')
                  .assign(Account_Holder_ID=lambda df_x: df_x['Account_Holder_ID'].astype(int))
                  .drop(columns='Account Holder ID')
                  .rename(columns=lambda c: c.replace('_', ' ')) )


# account holders
df_accthold = ( pd.read_csv(r'.\inputs\Account Holders.csv',
                            parse_dates=['Date of Birth'],
                            dayfirst=True)
                  .assign(Contact_Number=lambda df_x: df_x['Contact Number']
                                                          .astype(str)
                                                          .str.replace('^7', '07', regex=True)) )


# transaction detail
df_txndtl = ( pd.read_csv(r'.\inputs\Transaction Detail.csv',
                          parse_dates=['Transaction Date'],
                          dayfirst=True)
                .query("`Cancelled?` == 'N' & Value >= 1000") )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# join the tables together
df_out = ( df_txndtl
              .merge(df_txnpath.rename(columns={'Account From' : 'Account Number'}),
                     on='Transaction ID',
                     how='inner')
              .merge(df_acctinfo,
                     on='Account Number',
                     how='inner')
              .merge(df_accthold,
                     on='Account Holder ID',
                     how='inner') )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2023-07.csv', 
              index=False,
              date_format='%d/%m/%Y',
              columns=['Transaction ID', 'Account To', 'Transaction Date', 'Value', 'Name',
                       'Date of Birth', 'Contact Number', 'First Line of Address',
                       'Account Number', 'Account Type', 'Balance Date', 'Balance'])


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
