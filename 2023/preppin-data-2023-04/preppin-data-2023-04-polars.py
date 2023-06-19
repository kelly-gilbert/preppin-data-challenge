# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 04 - New Customers
https://preppindata.blogspot.com/2023/01/2023-week-4-new-customers.html

- Input data
- We want to stack the tables on top of one another, since they have the same 
  fields in each sheet. 
  We can do this one of 2 ways:
  - Drag each table into the canvas and use a union step to stack them on top 
    of one another
  - Use a wildcard union in the input step of one of the tables
- Some of the fields aren't matching up as we'd expect, due to differences in 
  spelling. Merge these 
  fields together
- Make a Joining Date field based on the Joining Day, Table Names and the year 2023
- Now we want to reshape our data so we have a field for each demographic, for each new customer
- Make sure all the data types are correct for each field
- Remove duplicates
  - If a customer appears multiple times take their earliest joining date
- Output the data

Author: Kelly Gilbert
Created: 2023-06-18
Requirements:
  - input dataset:
      - New Customers.xlsx
  - output dataset (for results check only):
      - 2023 Week 4 Output.csv
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# function
#---------------------------------------------------------------------------------------------------

def rename_if_exists(c, map_dict):
    """
    rename columns using a dictionary, or return the original field if it is not in the dict
    """
    
    return map_dict[c] if c in map_dict.keys() else c


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

field_renames = { 'Demographiic' : 'Demographic', 
                  'Demagraphic' : 'Demographic' }


df = ( pl.concat(
                  [
                    ( v.select(pl.all().map_alias(lambda c: rename_if_exists(c, field_renames)))
                       .with_columns(pl.lit(k).alias('Month')) )
                    for k, v 
                    in pl.read_excel(r'.\inputs\New Customers.xlsx', sheet_id=0).items()
                  ] 
         )
    
         # make the joining date field
         .with_columns((pl.col('Month') + '-' 
                        + pl.col('Joining Day').cast(pl.Utf8()) 
                        + pl.lit('-2023')).str.to_date(format='%B-%d-%Y').alias('Joining Date'))
         
         # pivot demographics into columns
         .pivot(index=['ID', 'Joining Date'], 
                columns='Demographic', 
                values='Value', 
                aggregate_function='first')
         
         # keep the record with the first joining date by ID
         .sort(pl.col('Joining Date'))
         .unique(subset='ID')
         
         # change the date of birth to date
         .with_columns(pl.col('Date of Birth').str.to_date(format='%m/%d/%Y'))
     )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.write_csv(r'.\outputs\output-2023-04.csv', date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2023 Week 4 Output.csv']
my_files = [r'.\outputs\output-2023-04.csv']
unique_cols = [['ID']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
