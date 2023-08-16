# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 31 - HR Month - Filling in Missing IDs (polars)
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
Created: 2023-08-14
Requirements:
  - input datasets:
      - ee_dim_input
      - ee_monthly_input
  - output datasets (for results check only):
      - ee_dim_v2
      - ee_monthly_v2
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


# --------------------------------------------------------------------------------------------------
# function
# --------------------------------------------------------------------------------------------------

def fill_replace(col1, col2, lookup_dict):
    """ 
    fill col1 by looking up col2 in the lookup_dict. If col2 is NaN, use the original col1 value
    """
    
    return ( pl.when(col2.is_null() | ~col2.is_in(lookup_dict.keys()))
               .then(col1)
               .otherwise(col2.map_dict(lookup_dict, default=pl.first())) )


# --------------------------------------------------------------------------------------------------
# input the data
# --------------------------------------------------------------------------------------------------

df_ee = pl.scan_csv(r'.\inputs\ee_dim_input.csv')
df_mo = pl.scan_csv(r'.\inputs\ee_monthly_input.csv')


# --------------------------------------------------------------------------------------------------
# process the data
# --------------------------------------------------------------------------------------------------

# build lookup dicts
lookup_guid = dict( 
                  pl.concat(
                      [(df_ee
                            .select(pl.col(['guid', 'employee_id']))
                            .drop_nulls()
                       ),
                       (df_mo
                            .select(pl.col(['guid', 'employee_id']))
                            .drop_nulls()
                       )]
                  )
                  .unique()
                  .collect()
                  .iter_rows()
              )

lookup_eeid = { v:k for k, v in lookup_guid.items() }


# fill in missing values
df_ee = ( df_ee
              .with_columns(
                  fill_replace(pl.col('employee_id'), 
                               pl.col('guid'), 
                               lookup_guid),
                  fill_replace(pl.col('guid'),
                               pl.col('employee_id'),
                               lookup_eeid) 
              )
        )

df_mo = ( df_mo
              .with_columns(
                  fill_replace(pl.col('employee_id'), 
                               pl.col('guid'), 
                               lookup_guid),
                  fill_replace(pl.col('guid'),
                               pl.col('employee_id'),
                               lookup_eeid) 
              )
        )


# --------------------------------------------------------------------------------------------------
# output the data
# --------------------------------------------------------------------------------------------------

( df_mo
      .collect()
      .write_csv(r'.\outputs\output-2023-31-ee_monthly_v2.csv',
                 date_format='%d/%m/%Y')
)

( df_ee
      .collect()
      .write_csv(r'.\outputs\output-2023-31-ee_dim_v2.csv',
                 date_format='%d/%m/%Y')
)


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



#---------------------------------------------------------------------------------------------------
# alternative method using joins
#---------------------------------------------------------------------------------------------------

# method 1 (map_dict, above) = 24 ms ± 2.98 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# method 2 (joins, below) = 28.1 ms ± 2.34 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)


# input the data (same as method #1)
df_ee = pl.scan_csv(r'.\inputs\ee_dim_input.csv')
df_mo = pl.scan_csv(r'.\inputs\ee_monthly_input.csv')


# create the lookup df
df_lookup = ( pl.concat(
                      [(df_ee
                            .select(pl.col(['guid', 'employee_id']))
                            .drop_nulls()
                       ),
                       (df_mo
                            .select(pl.col(['guid', 'employee_id']))
                            .drop_nulls()
                       )]
                  )
                  .unique()
              )


# process the data (use joins)
df_ee = ( df_ee
              .join(df_lookup, 
                    on='guid', 
                    how='left')
              .join(df_lookup,
                    on='employee_id',
                    how='left')
              .with_columns( 
                  pl.col('employee_id').fill_null(pl.col('employee_id_right')),
                  pl.col('guid').fill_null(pl.col('guid_right'))
              )
              .select(df_ee.columns)
              
        )

df_mo = ( df_mo
              .join(df_lookup, 
                    on='guid', 
                    how='left')
              .join(df_lookup,
                    on='employee_id',
                    how='left')
              .with_columns( 
                  pl.col('employee_id').fill_null(pl.col('employee_id_right')),
                  pl.col('guid').fill_null(pl.col('guid_right'))
              )
              .select(df_mo.columns)
              
        )

# output the data (same as method #1)
( df_mo
      .collect()
      .write_csv(r'.\outputs\output-2023-31-ee_monthly_v2.csv',
                 date_format='%d/%m/%Y')
)

( df_ee
      .collect()
      .write_csv(r'.\outputs\output-2023-31-ee_dim_v2.csv',
                 date_format='%d/%m/%Y')
)
