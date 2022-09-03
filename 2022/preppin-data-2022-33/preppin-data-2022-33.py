# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 33 - C&BSCo Next Sale
https://preppindata.blogspot.com/2022/08/2022-week-33-c-next-sale.html

- Input the data sets
- Link the Instore and Online sales together to be one data source
- Call the Nulls in the Stores field Online 
- Link in the product Lookup to name the products instead of having their ID number
- Create the 'Product Type' field by taking the first word of the product name
- Create a data set from your work so far that includes the next sale after the one made in the 
  SAME store of the same product type 
- Requirement updated 20th Aug 2022
- Workout how long it took between the original sale and the next sale in minutes
- Remove any negative differences. These are sales that got refunded. 
- Create a data set that shows the average of these values for each store and product type. Call 
  this field 'Average mins to next sale' 
- Output the results

Author: Kelly Gilbert
Created: 2022-09-01
Requirements:
  - input dataset:
      - PD 2022 Week 33 Input Instore Orders.csv
      - PD 2022 Week 33 Input Online Orders.csv
      - Preppin' Summer 2022 - Product Lookup.csv
  - output dataset (for results check only):
      - PD 2022 Wk 33 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_sales = ( pd.concat([pd.read_csv(r'.\inputs\PD 2022 Week 33 Input Instore Orders.csv',
                                    parse_dates=['Sales Date'], dayfirst=True)
                          .rename(columns={'Sales Date' : 'Sales Timestamp'}),
                        pd.read_csv(r'.\inputs\PD 2022 Week 33 Input Online Orders.csv', 
                                    parse_dates=['Sales Timestamp'], dayfirst=True)\
                          .assign(Store='Online')])
           )
                                                        
df_lookup = ( pd.read_csv(r".\inputs\Preppin' Summer 2022 - Product Lookup.csv")
                .assign(Product_Type = lambda df_x: df_x['Product Name'].str.extract('(.*) - .*'))
                .rename(columns=lambda c: c.replace('_', ' '))
            )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# return the product type for the product ID
df_sales['Product Type'] = df_sales['Product'].replace({k:v for k,v in zip(df_lookup['Product ID'], 
                                                                           df_lookup['Product Type'])})


# find the time between each sale (by store and product type)
df_sales = df_sales.sort_values(by=['ID'])

df_merge = pd.merge_asof(df_sales, 
                         df_sales[['Store', 'Product Type', 'ID', 'Sales Timestamp']]
                             .rename(columns={'Sales Timestamp' : 'Next Timestamp'}), 
                         by=['Store', 'Product Type'], 
                         on='ID',
                         allow_exact_matches=False, direction='forward')

df_merge['time_diff_min'] = (df_merge['Next Timestamp'] 
                             - df_merge['Sales Timestamp']).dt.total_seconds() / 60


# summarize by product type and store
df_out = ( df_merge[df_merge['time_diff_min'] >= 0]
               .groupby(['Product Type', 'Store'], as_index=False)['time_diff_min'].mean().round(1)
               .rename(columns={'time_diff_min' : 'Average mins to next sale'})
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-33.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 33 Output.csv']
my_files = [r'.\outputs\output-2022-33.csv']
unique_cols = [['Store', 'Product Type']]
col_order_matters = False
round_dec = 3

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
