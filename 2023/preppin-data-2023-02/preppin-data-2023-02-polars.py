# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 02 - International Bank Account Numbers (Polars version)
https://preppindata.blogspot.com/2023/01/2023-week-2-international-bank-account.html

- Input the data
- In the Transactions table, there is a Sort Code field which contains dashes. We need to remove
  these so just have a 6 digit string
- Use the SWIFT Bank Code lookup table to bring in additional information about the SWIFT code and 
  Check Digits of the receiving bank account
- Add a field for the Country Code
  - Hint: all these transactions take place in the UK so the Country Code should be GB
- Create the IBAN as above
  - Hint: watch out for trying to combine sting fields with numeric fields - check data types
- Remove unnecessary fields
- Output the data

Author: Kelly Gilbert
Created: 2023-06-17
Requirements:
  - input dataset:
      - Transactions.csv
      - Swift Codes.csv
  - output dataset (for results check only):
      - IBAN Output.csv
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

# merge the two datasets
df = ( pl.read_csv(r'.\inputs\Transactions.csv')
         .with_columns(pl.lit('GB').alias('Country Code')) 
         .join(pl.read_csv(r'.\inputs\Swift Codes.csv'),
               on='Bank',
               how='left')
         .with_columns( 
             ( pl.col('Country Code')
               + pl.col('Check Digits').cast(pl.Utf8)
               + pl.col('SWIFT code')
               + pl.col('Sort Code').str.replace_all('-', '', literal=True) 
               + pl.col('Account Number').cast(pl.Utf8) ).alias('IBAN')
         )
      )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

( df.select([ pl.col('Transaction ID'), 
              pl.col('IBAN') ])
    .write_csv(r'.\outputs\output-2023-02.csv') )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\IBAN Output.csv']
my_files = [r'.\outputs\output-2023-02.csv']
unique_cols = [['Transaction ID']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
