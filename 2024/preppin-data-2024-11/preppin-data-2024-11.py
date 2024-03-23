# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 11 - 13 months in a year
https://preppindata.blogspot.com/2024/03/2024-week-11-13-months-in-year.html

- Input the data
- Create a row for each day of the year
  - I've chosen to use 2024 for the challenge so results will be different if you select a 
    non-leap year
- Calculate the new months of the year such that the first 28 days of the month are month 1, the 
  next 28 days are month 2, etc
  - This will give you 14 months, with the 14th month containing just 2 days
- Create a new date with the format:
  - New day of the month / New month / 2024
  - e.g. 20/11/2024 becomes 17/12/2024
- Filter the data to only contain dates for which the month has changed in the new system
- Output the data

Author: Kelly Gilbert
Created: 2024-03-19
Requirements:
  - input dataset:
      - 2024W11 Input.csv
  - output dataset (for results check only):
      - 2024W11 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

YEAR = 2024


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_in = ( pd.read_csv(r'.\inputs\2024W11 Input.csv')
            .assign(Date = lambda df_x: pd.to_datetime(df_x['Date'] + f', {YEAR}')) )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df = pd.DataFrame({ 'Date' : pd.date_range(df_in.iloc[0, 0],
                                           df_in.iloc[1, 0],
                                           freq='1D')})

df['new_month'] = (df['Date'].dt.dayofyear - 1) // 28 + 1
df['new_day'] = (df['Date'].dt.dayofyear - 1) % 28 + 1

df['New Date'] = ( df['new_day'].astype(str).str.zfill(2) + '/' 
                   + df['new_month'].astype(str).str.zfill(2) 
                   + '/' + str(YEAR) )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# output only the changed months
( df.query("new_month != Date.dt.month")
    [['Date', 'New Date']]
    .to_csv(r'.\outputs\output-2024-11.csv',
            index=False,
            date_format='%d/%m/%Y') )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2024W11 Output.csv']
my_files = [r'.\outputs\output-2024-11.csv']
unique_cols = [['Date']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
