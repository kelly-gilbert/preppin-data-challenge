# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 29 - C&BSco Meeting Targets?
https://preppindata.blogspot.com/2022/07/2022-week-29-c-meeting-targets.html

- Input both data sets
- Remove unnecessary values from the Product Name field to just leave the Product Type
- Total Sales for each Store and Product Type
- Change the Targets data set into three columns
  - Product
  - Store
  - Sales Target (k's)
- Multiple the Sales Target (k's) by 1000 to create the full sales target number (i.e. 75 becomes 75000)
- Prepare your data sets for joining together by choosing your next step:
  - Easy - make your Sales input Product Type and Store name UPPER CASE
  - Hard - make your Targets' Store and Product fields TitleCase
- Join the data sets together and remove any duplicated fields
- Calculate whether each product in each store beats the target
- Output the results

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input datasets:
      - Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv
      - Preppin' Summer 2022 - Targets (k's).csv
  - output dataset (for results check only):
      - PD 2022 Wk 29 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for comparing my results to the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in the sales data, extract the product type, sum sales by product type/store
df = ( pd.read_csv(r".\inputs\Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv")
         .assign(PRODUCT=lambda df_x: df_x['Product Name'].str.extract('(.*?) - .*'))
         .groupby(['PRODUCT', 'Store Name', 'Region'], as_index=False)['Sale Value'].sum()
     )

df_target = pd.read_csv(r".\inputs\Preppin' Summer 2022 - Targets (k's).csv")


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# reshape and prep the Targets data
df_target = df_target.melt(id_vars='PRODUCT', var_name='Store Name', value_name="Sales Target (k's)")

df_target['Target'] = df_target["Sales Target (k's)"] * 1000
df_target['PRODUCT'] = df_target['PRODUCT'].str.title()
df_target['Store Name'] = df_target['Store Name'].str.title()


# join the datasets together
df_out = df.merge(df_target, on=['PRODUCT', 'Store Name'], how='left')    
   

# calculate whether each product in each store beats the target
df_out['Beats Target?'] = df_out['Sale Value'] > df_out['Target']


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-29.csv', index=False, 
              columns=['Beats Target?', 'Target', 'Store Name', 'Region', 'Sale Value', 'PRODUCT'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 29 Output.csv']
my_files = [r'.\outputs\output-2022-29.csv']
unique_cols = [['Store Name', 'PRODUCT']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
