# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 18 - Un-pivoting
https://preppindata.blogspot.com/2022/05/2022-week-18-un-pivoting.html

- Input the data
- Dynamically rename the fields so that there is a common separator between the Bike Type, Date and 
  Measure Name
- Pivot the data
- Split out the Bike Type, Date and Measure Name
- Create a field for Sales and Profit
- Output the data

Author: Kelly Gilbert
Created: 2022-05-14
Requirements:
  - input dataset:
      - 2022W18 Input.csv
  - output dataset (for results check only):
      - 2022W18 Output.csv
  - output_check module (for results check only)\
      
"""


import pandas as pd
import output_check  # custom module for comparing output to the solution file


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\2022W18 Input.csv')\
       .melt(id_vars='Region')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split out the Bike Type, Date and Measure Name
df[['Bike Type', 'Month', 'Measure Name']] = df['variable'].str.extract('(\w+?)_+(\w{3}_\d+)_+(\w+)')

# convert the month to datetime
df['Month'] = pd.to_datetime(df['Month'], format='%b_%y')

# pivot sales and profit into separate columns
df_out = df.pivot_table(index=['Region', 'Bike Type', 'Month'], values='value', columns='Measure Name',
                        aggfunc='sum')\
           .reset_index()


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-18.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W18 Output.csv']
my_files = [r'.\outputs\output-2022-18.csv']
unique_cols = [['Bike Type', 'Month', 'Region']]
col_order_matters = True
round_dec = 8

output_check.output_check(solution_files, my_files, unique_cols, col_order_matters = False)
