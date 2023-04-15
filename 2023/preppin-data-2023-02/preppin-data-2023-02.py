# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 02 - International Bank Account Numbers
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
Created: 2023-04-15
Requirements:
  - input dataset:
      - Transactions.csv
      - Swift Codes.csv
  - output dataset (for results check only):
      - IBAN Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# merge the two datasets
df = ( pd.read_csv(r'.\inputs\Transactions.csv')
         .merge(pd.read_csv(r'.\inputs\Swift Codes.csv'),
                on='Bank',
                how='left') )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# add the country code
df['Country Code'] = 'GB'


# construct the IBAN
df['IBAN'] = ( df['Country Code'] 
              + df['Check Digits'].astype(str) 
              + df['SWIFT code'] 
              + df['Sort Code'].str.replace('-', '') 
              + df['Account Number'].astype(str) )
 

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2023-02.csv', index=False, columns=['Transaction ID', 'IBAN'])


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
