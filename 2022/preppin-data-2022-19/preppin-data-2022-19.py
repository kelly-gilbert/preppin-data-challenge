# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 19 - C&BSCo Good Sales but Wrong Sizes
https://preppindata.blogspot.com/2022/05/2022-week-19-c-good-sales-but-wrong.html

- Input all three sheets of data
- Change the Size ID to an actual Size value in the Sales table
- Link the Product Code to the Sales Table to provide the Scent information
- Create an Output that contains the products sold that have the sizes recorded correctly (Output 1)
- Create another data set that contains all the Products sold with the incorrect sizes and what the 
  sizes should have been
- Aggregate this data to show each Product Sold, the Scent and the Size it should be with how many 
  sales have incorrectly been recorded for each. 
- Output
    - Output 1: Correctly Recorded Sales
    - Output 2: Wrongly Recorded Sales

Author: Kelly Gilbert
Created: 2022-05-15
Requirements:
  - input dataset:
      - PD 2022 Wk 19 Input.xlsx
  - output dataset (for results check only):
      - PD 2022 Wk 19 Correct Sizes.csv
      - PD 2022 Wk 19 Wrong Sizes.csv

"""


import pandas as pd
import output_check  # custom module for comparing output to the solution file


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\PD 2022 Wk 19 Input.xlsx') as xl:
    df_sales = pd.read_excel(xl, sheet_name='Sales')                
    df_sizes = pd.read_excel(xl, sheet_name='Size Table')
    df_prod = ( pd.read_excel(xl, sheet_name='Product Set')\
                  .rename(columns={'Size' : 'Product Size'}) )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# remove S from product ID in products table
df_prod['Product Code'] = df_prod['Product Code'].str.replace('S', '')


# get the actual size for each size ID
df_sales['Sold Size'] = df_sales['Size'].replace(dict(zip(df_sizes['Size ID'], df_sizes['Size'])))
                 

# join to the product table to get the scent and correct size
df_out = df_sales.merge(df_prod, left_on='Product', right_on='Product Code', how='left')


# remove decimals for output
df_out[['Sold Size', 'Product Size']] = ( df_out[['Sold Size', 'Product Size']]
                                             .astype(str)
                                             .replace('\.0', '', regex=True) )


#---------------------------------------------------------------------------------------------------
# output the files
#---------------------------------------------------------------------------------------------------

# output 1: correct sizes
( df_out[df_out['Sold Size'] == df_out['Product Size']]
      .to_csv(r'.\outputs\output-2022-19-correct.csv', index=False,
              columns=['Product Size', 'Scent', 'Product', 'Store']) )


# output 2: wrong sizes (count of sales by product)
( df_out[~(df_out['Sold Size'] == df_out['Product Size'])]
      .groupby(['Product Code', 'Product Size', 'Scent'], as_index=False)
      .agg(Sales_with_the_wrong_size=('Store', 'count'))
      .rename(columns=lambda x: x.replace('_', ' '))
      .to_csv(r'.\outputs\output-2022-19-wrong.csv', index=False,
                columns=['Sales with the wrong size', 'Product Code', 'Product Size', 'Scent']) )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 19 Correct Sizes.csv', 
                  r'.\outputs\PD 2022 Wk 19 Wrong Sizes.csv']
my_files = [r'.\outputs\output-2022-19-correct.csv', r'.\outputs\output-2022-19-wrong.csv']
unique_cols = [['Product Size', 'Scent', 'Product', 'Store'], 
               ['Product Code', 'Product Size', 'Scent']]
col_order_matters = True
round_dec = 8

output_check.output_check(solution_files, my_files, unique_cols, col_order_matters = False)
