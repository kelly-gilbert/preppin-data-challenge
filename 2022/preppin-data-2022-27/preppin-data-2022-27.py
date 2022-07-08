# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 27 - C&BSCo Clean and Aggregate
https://preppindata.blogspot.com/2022/07/2022-week-27-c-clean-and-aggregate.html

- Input the data
- Separate out the Product Name field to form Product Type and Quantity
- Rename the fields to 'Product Type' and 'Quantity' respectively
- Create two paths in your flow: 
  - One to deal with the data about Liquid Soap sales
  - One to deal with the data about Bar Soap sales
- For each path in your flow:
  - Clean the Quantity field to just leave values
    - For Liquid, ensure every value is in millilitres 
  - Sum up the sales for each combination of Store, Region and Quantity
  - Also, count the number of orders that has the combination of Store, Region and Quantity. Name this field 'Present in N orders' 
- Output each file from the separate paths

Author: Kelly Gilbert
Created: 2022-07-07
Requirements:
  - input dataset:
      - Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv
  - output dataset (for results check only):
      - PD 2022 Wk 27 Bars Output.csv
      - PD 2022 Wk 27 Liquid Output.csv
"""


from numpy import where
import pandas as pd
import output_check  # custom module for comparing output to the solution file


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r".\inputs\Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv", 
                 parse_dates=['Sale Date'], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data (no split)
#---------------------------------------------------------------------------------------------------

# separate out the Product Name field to form Product Type and Quantity
df[['Product Type', 'Original Quantity', 'Unit']] = df['Product Name'].str.extract('(.+?) - (\d+)(.*)')


# for liquid, ensure every value is in milliliters
df['Quantity'] =  df['Original Quantity'].astype(int) * where(df['Unit'] == 'L', 1000, 1)


# sum sales and count orders by store, region, and quantity
df_out = ( df.groupby(['Product Type', 'Store Name', 'Region', 'Quantity'], as_index=False)
             .agg(Sale_Value=('Sale Value', 'sum'),
                  Present_in_N_orders=('Order ID', 'nunique'))
             .rename(columns=lambda x: x.replace('_', ' '))             
         )


#---------------------------------------------------------------------------------------------------
# output the file (no split)
#---------------------------------------------------------------------------------------------------

for t in df_out['Product Type'].unique(): 
    ( df_out[df_out['Product Type']==t]
          .drop(columns=['Product Type'])
          .to_csv(f'.\\outputs\\output-2022-27-{t}.csv', index=False)

    )


#---------------------------------------------------------------------------------------------------
# process the data (split path)
#---------------------------------------------------------------------------------------------------

# separate out the Product Name field to form Product Type and Quantity
df[['Product Type', 'Quantity', 'Unit']] = df['Product Name'].str.extract('(.+?) - (\d+)(.*)')


# split the data based on product type
df_bar = df.loc[df['Product Type']=='Bar', df.columns]
df_liquid = df.loc[df['Product Type']=='Liquid', df.columns]


# for liquid, ensure every value is in milliliters
df_liquid['Quantity'] =  df['Quantity'].astype(int) * where(df['Unit'] == 'L', 1000, 1)


#---------------------------------------------------------------------------------------------------
# output the file (split path)
#---------------------------------------------------------------------------------------------------

for df_x in [df_bar, df_liquid]: 
    product_type = df['Product Type'].max()

    ( df_x.groupby(['Store Name', 'Region', 'Quantity'], as_index=False)
          .agg(Sale_Value=('Sale Value', 'sum'),
               Present_in_N_orders=('Order ID', 'nunique'))
          .rename(columns=lambda x: x.replace('_', ' '))             
          .to_csv(f'.\\outputs\\output-2022-27-{product_type}.csv', index=False)
    )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 27 Bars Output.csv', 
                  r'.\outputs\PD 2022 Wk 27 Liquid Output.csv']
my_files = [r'.\outputs\output-2022-27-Bar.csv', r'.\outputs\output-2022-27-Liquid.csv']
unique_cols = [['Store Name', 'Region', 'Quantity'], ['Store Name', 'Region', 'Quantity']]
col_order_matters = False
round_dec = 2

output_check.output_check(solution_files, my_files, unique_cols, col_order_matters = False)
