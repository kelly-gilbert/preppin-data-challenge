# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 41 - Dynamic Times Tables
https://preppindata.blogspot.com/2022/10/2022-week-41-dynamic-times-tables.html

- Input data 
- Create a parameter that allows the user to set the multiplication grid they want
- Output the data

Author: Kelly Gilbert
Created: 2022-10-13
Requirements:
  - None
"""


from itertools import product
import pandas as pd
import sys


def get_input():
    """
    If the user enters a valid number >= 1, returns the number.
    Otherwise, continues asking (or exists if the user hits Enter)
    """
    
    while True:
        input_val = input('Please enter a whole number (1 or greater):')
        if input_val == '':
            sys.exit()
        elif str(input_val).isnumeric():
            return int(input_val)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

num_list = range(1, get_input() + 1)

# create all combinations of the number list, multiply, pivot multipliers into columns
df = ( pd.DataFrame(list(product(num_list, num_list)), columns=['Number', 'Multiplier'])
         .assign(Product = lambda df_x: df_x['Number'] * df_x['Multiplier']) 
         .pivot_table(index='Number', columns='Multiplier', values='Product', aggfunc='first') )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-41.csv', index=True)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week

