# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 44 - Creating Order IDs
https://preppindata.blogspot.com/2022/11/2022-week-44-creating-order-ids.html

- Input the data
- Aside from our Order Number issue, you'll notice we have 3 fields for Order Dates. 
  Bring these together into a single field
- We want our new Order IDs to have the following structure:
  - The first 2 characters should be the Customers initials
  - The last characters should be the Order Number
  - If necessary, there should be 0's in between to create 8 characters for the Order ID length
    - For example: AJ000746
- Output the data

Author: Kelly Gilbert
Created: 2022-11-03
Requirements:
  - input dataset:
      - 2022W44 Input.csv
  - output dataset (for results check only):
      - 2022W44 Output.csv
"""

from numpy import where
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\2022W44 Input.csv', 
                 parse_dates=['Order Date', 'Date of Order', 'Purchase Date'], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# combine the date fields
df['Order Date'] = where(df['Order Date'].notna(), df['Order Date'],
                          where(df['Date of Order'].notna(), df['Date of Order'],
                                df['Purchase Date']))   


# generate the order ID
df['Order ID'] = ( df['Customer'].str.findall('(?:^|\s)(.).*?')
                                 .str.join('')
                   + df['Order Number'].astype(str).str.zfill(6) )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-44.csv', index=False, date_format='%d/%m/%Y',
          columns=['Order ID', 'Order Number', 'Customer', 'Order Date'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W44 Output.csv']
my_files = [r'.\outputs\output-2022-44.csv']
unique_cols = [['Customer', 'Order Number']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)



#---------------------------------------------------------------------------------------------------
# timing different options for combining the dates
#---------------------------------------------------------------------------------------------------

# option 1: combine_first
# 1.13 ms ± 35.5 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%%timeit
df['Order Date2'] = ( df['Order Date'].combine_first(df['Date of Order'])
                                      .combine_first(df['Purchase Date']) )


# option 2: ffill
# 1.35 ms ± 117 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%%timeit
df['Order Date2'] = df[['Order Date', 'Date of Order', 'Purchase Date']].ffill(axis=1).iloc[:,2]


# option 3: numpy
# 928 µs ± 18.2 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each))

%%timeit 
import numpy as np

v = df[['Order Date', 'Date of Order', 'Purchase Date']].values
j = np.isnan(v).argmin(1)
df['Order Date2'] = v[np.arange(len(v)), j]
    
    
# option 4: where
# 475 µs ± 22.1 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)

%%timeit
from numpy import where

df['Order Date2'] = where(df['Order Date'].notna(), df['Order Date'],
                          where(df['Date of Order'].notna(), df['Date of Order'],
                                df['Purchase Date']))   
