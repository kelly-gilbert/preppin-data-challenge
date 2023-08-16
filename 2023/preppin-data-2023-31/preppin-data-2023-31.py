# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 31 - HR Month - Filling in Missing IDs
https://preppindata.blogspot.com/2023/08/2023-week-31-hr-month-filling-in.html

- Input the data
- Create a lookup table:
  - Find the unique employee_id / guid combinations in each table
  - Union the results together and remove any duplicates
  - Filter out any rows where one of the IDs is missing
- Join the main table with the lookup table on employee_id (make sure to keep all records from the original table, whether or not they match)
- If the guid is missing from the main table, replace it with the guid from the lookup table.
- Join the result to the lookup table on guid (make sure to keep all records from the original table, whether or not they match)
- If the employee_id is missing from the main table, replace it with the value from the lookup table
- Repeat previous steps for both the employee table and the monthly table.
- Make sure that there are no nulls in the employee_id and guid fields in both tables
- Output the results (two files)

Author: Kelly Gilbert
Created: 2023-08-11
Requirements:
  - input datasets:
      - ee_dim_input
      - ee_monthly_input
  - output datasets (for results check only):
      - ee_dim_v2
      - ee_monthly_v2
"""


from numpy import where
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


# --------------------------------------------------------------------------------------------------
# function
# --------------------------------------------------------------------------------------------------

def fill_replace(col1, col2, lookup_dict):
    """ 
    fill col1 by looking up col2 in the lookup_dict. If col2 is NaN, use the original col1 value
    """
    
    return where(col2.isna() | ~col2.isin(lookup_dict.keys()), col1, col2.replace(lookup_dict))


# --------------------------------------------------------------------------------------------------
# input the data
# --------------------------------------------------------------------------------------------------

df_ee = pd.read_csv(r'.\inputs\ee_dim_input.csv')
df_mo = pd.read_csv(r'.\inputs\ee_monthly_input.csv')


# --------------------------------------------------------------------------------------------------
# process the data
# --------------------------------------------------------------------------------------------------

# build lookup dicts
lookup_guid = ( pd.concat([df_ee[['guid', 'employee_id']],
                           df_mo[['guid', 'employee_id']]])
                  .dropna(how='any')
                  .drop_duplicates()
                  .set_index('guid')
                  .squeeze()
                  .to_dict() )

lookup_eeid = { v:k for k, v in lookup_guid.items() }


# apply lookups to fill in missing values
df_ee['employee_id'] = fill_replace(df_ee['employee_id'], df_ee['guid'], lookup_guid)
df_ee['guid'] = fill_replace(df_ee['guid'], df_ee['employee_id'], lookup_eeid)

df_mo['employee_id'] = fill_replace(df_mo['employee_id'], df_mo['guid'], lookup_guid)
df_mo['guid'] = fill_replace(df_mo['guid'], df_mo['employee_id'], lookup_eeid)


# --------------------------------------------------------------------------------------------------
# output the data
# --------------------------------------------------------------------------------------------------

df_mo.to_csv(r'.\outputs\output-2023-31-ee_monthly_v2.csv',
             date_format='%d/%m/%Y',
             index=False)
              
df_ee.to_csv(r'.\outputs\output-2023-31-ee_dim_v2.csv',
             date_format='%d/%m/%Y',
             index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\ee_dim_v2.csv',
                  r'.\outputs\ee_monthly_v2.csv']
my_files = [r'.\outputs\output-2023-31-ee_dim_v2.csv',
            r'.\outputs\output-2023-31-ee_monthly_v2.csv']
unique_cols = [['employee_id'], 
               ['employee_id', 'month_end_date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
