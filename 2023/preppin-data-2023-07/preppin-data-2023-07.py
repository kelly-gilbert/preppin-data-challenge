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

with ExcelFile(r'.\inputs\', parse_dates=[]) as xl:
    df = pd.read_excel(xl, sheet_name=)

df = pd.read_csv(r'.\inputs\', parse_dates=[], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2023-07.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\]
my_files = [r'.\outputs\output-2023-07.csv']
unique_cols = [['col1']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
