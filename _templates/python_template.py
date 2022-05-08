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
  - output_check module (for results check only)

"""


import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

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

solution_files = ['']
my_files = ['output-YYYY-WW.csv']
unique_cols = ['Month']
col_order_matters = True
round_dec = 8

output_check.output_check(solution_files, my_files, unique_cols, col_order_matters = False)
