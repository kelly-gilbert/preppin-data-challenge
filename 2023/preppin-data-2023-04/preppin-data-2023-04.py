# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 04 - New Customers
https://preppindata.blogspot.com/2023/01/2023-week-4-new-customers.html

- Input data
- We want to stack the tables on top of one another, since they have the same fields in each sheet. 
  We can do this one of 2 ways:
  - Drag each table into the canvas and use a union step to stack them on top of one another
  - Use a wildcard union in the input step of one of the tables
- Some of the fields aren't matching up as we'd expect, due to differences in spelling. Merge these 
  fields together
- Make a Joining Date field based on the Joining Day, Table Names and the year 2023
- Now we want to reshape our data so we have a field for each demographic, for each new customer
- Make sure all the data types are correct for each field
- Remove duplicates
  - If a customer appears multiple times take their earliest joining date
- Output the data

Author: Kelly Gilbert
Created: 2023-04-15
Requirements:
  - input dataset:
      - New Customers.xlsx
  - output dataset (for results check only):
      - 2023 Week 4 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

field_renames = { 'Demographiic' : 'Demographic', 
                  'Demagraphic' : 'Demographic', }


with pd.ExcelFile(r'.\inputs\New Customers.xlsx') as xl:
    df = pd.concat([( pd.read_excel(xl, sheet_name=s)
                        .assign(Month=s)
                        .rename(columns=field_renames) )
                    for s in xl.sheet_names])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# make the joining date field
df['Joining Date'] = pd.to_datetime(df['Month'] + ' ' + df['Joining Day'].astype(str) + ', 2023')


# reshape demographic types into cols, keeping the first join date by ID
df_out = ( pd.pivot_table(df, 
                          index=['ID', 'Joining Date'], 
                          columns='Demographic', 
                          values='Value', 
                          aggfunc='min')
             .reset_index()
             .sort_values('Joining Date')
             .drop_duplicates('ID') )


# change data types
df_out['Date of Birth'] = pd.to_datetime(df_out['Date of Birth'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2023-04.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2023 Week 4 Output.csv']
my_files = [r'.\outputs\output-2023-04.csv']
unique_cols = [['ID']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
