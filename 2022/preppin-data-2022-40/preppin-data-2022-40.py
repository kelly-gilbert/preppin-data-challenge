# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 40 - Times Tables
https://preppindata.blogspot.com/2022/10/2022-week-40-times-tables.html

- Input data 
- Create a 9x9 multiplication table
- Output the data

Author: Kelly Gilbert
Created: 2022-10-05
Requirements:
  - input dataset:
      - PD 2022 Wk 40 Input.csv
  - output dataset (for results check only):
      - PD 2022 Wk 40 Output.csv
"""


from itertools import product
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

nums = pd.read_csv(r'.\inputs\PD 2022 Wk 40 Input.csv')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

num_list = range(nums['Numbers'].min(), 
                 nums['Numbers'].max() + 1)

# create all combinations of the number list, multiply, pivot multipliers into columns
df = ( pd.DataFrame(list(product(num_list, num_list)), columns=['Number', 'Multiplier'])
         .assign(Product = lambda df_x: df_x['Number'] * df_x['Multiplier']) 
         .pivot_table(index='Number', columns='Multiplier', values='Product', aggfunc='first') )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-40.csv', index=True)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 40 Output.csv']
my_files = [r'.\outputs\output-2022-40.csv']
unique_cols = [['Number']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)



