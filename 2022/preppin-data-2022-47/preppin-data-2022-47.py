# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 47 - challenge title goes here
https://preppindata.blogspot.com/ - challenge url goes here

- Input data
- ...
- Output the data

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input dataset:
      - Chelsea Managers.xlsx
      - Chelsea Matches.csv
      - Prime Ministers.xlsx
  - output dataset (for results check only):
      - Chelsea Managers per Prime Minister.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\Chelsea Managers.xlsx') as xl:
    print(xl.sheet_names)


df_cm = pd.read_excel()


df = pd.read_csv(r'.\inputs\', parse_dates=[], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-47.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Chelsea Managers per Prime Minister.csv']
my_files = [r'.\outputs\output-2022-47.csv']
unique_cols = [['col1']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
