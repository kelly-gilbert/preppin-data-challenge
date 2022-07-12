# -*- coding: utf-8 -*-
"""
Preppin' Data YYYY: Week WW - challenge title goes here
https://preppindata.blogspot.com/ - challenge url goes here

- Input data
- ...
- Output the data

Author: Kelly Gilbert
Created: YYYY-MM-DD
Requirements:
  - input dataset:
      - 
  - output dataset (for results check only):
      - 
"""


import pandas as pd


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

df.to_csv(r'.\outputs\output-YYYY-WW.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\]
my_files = [r'.\outputs\output-YYYY-WW.csv']
unique_cols = [['col1']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
