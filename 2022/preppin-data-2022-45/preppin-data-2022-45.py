# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 45 - Strange Table Structure
https://preppindata.blogspot.com/2022/11/2022-week-45-strange-table-structure.html

- Input the data
- Split off the Year from the first row of data
- Pivot the remaining rows 
- Remove the 'F' from all of the F1, F2 etc field names so we have row numbers
- Reshape the data so each row has a Month associated with it
- Reshape the data so the values fall under either Sales or Profit
- Create a Date field using the Month and Year fields
- Output the data

Author: Kelly Gilbert
Created: 2022-11-11
Requirements:
  - input dataset:
      - Strange table structure.xlsx
  - output dataset (for results check only):
      - Week 45 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\Strange table structure.xlsx') as xl:
    year = pd.read_excel(xl, header=None, nrows=1, usecols=[0]).iloc[0, 0][-4:]
    df = pd.read_excel(xl, skiprows=1, header=[1,2])
    
    
#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------
    
# melt the columns into rows, then pivot metrics into cols
df_p = ( df.melt(id_vars=[df.columns[0]])
           .set_axis(['Store', 'Month', 'Metric', 'value'], axis=1)
           .pivot_table(values='value', 
                        index=['Store', 'Month'], 
                        columns='Metric', 
                        aggfunc='sum')
                      .reset_index() )

df_p['Date'] = pd.to_datetime(df_p['Month'] + ' ' + str(year))


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

( df_p.drop(columns='Month')
      .to_csv(r'.\outputs\output-2022-45.csv', index=False, date_format='%d/%m/%Y') )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Week 45 Output.csv']
my_files = [r'.\outputs\output-2022-45.csv']
unique_cols = [['Store', 'Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
