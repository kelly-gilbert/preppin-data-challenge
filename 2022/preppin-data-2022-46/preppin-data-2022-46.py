# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 46 - Dynamically Fixing Table Structures
https://preppindata.blogspot.com/2022/11/2022-week-46-dynamically-fixing-table.html

- Input the data
- Bring in the data from all the Regions and update the workflow so that no rows get duplicated
- Output the data

Author: Kelly Gilbert
Created: 2023-02-26
Requirements:
  - input dataset:
      - Strange table structure updated.xlsx
  - output dataset (for results check only):
      - Week 46 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def parse_file(xl, sheet_name):

    # read in the sheet data
    df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
        
    
    # month/value associated with each column #
    year = df.iloc[0,0][-4:]
    df_cols = ( df.iloc[2:4]
                  .T
                  .ffill()
                  .rename(columns={ 2 : 'month', 3 : 'metric' }) )
    df_cols['Date'] = pd.to_datetime(df_cols['month'] + ' ' + str(year))
    
    
    # reshape the data
    df_data = ( df.iloc[4:]
                  .rename(columns={ 0 : 'Store' })
                  .melt(id_vars='Store')
                  .merge(df_cols, left_on='variable', right_index=True)
                  .pivot_table(index=['Store', 'Date'], 
                               columns='metric', 
                               values='value', 
                               aggfunc='sum')
                  .reset_index() )

    return df_data.assign(Region=sheet_name)


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

in_path = r'.\inputs\Strange table structure updated.xlsx'

with pd.ExcelFile(in_path) as xl:
    df = pd.concat([parse_file(xl, s) for s in xl.sheet_names])
         

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-46.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Week 46 Output.csv']
my_files = [r'.\outputs\output-2022-46.csv']
unique_cols = [['Store', 'Region', 'Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
