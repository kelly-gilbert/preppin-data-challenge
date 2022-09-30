# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 39 - Filling in for HR
https://preppindata.blogspot.com/2022/09/2022-week-39-filling-in-for-hr.html

- Input the data
- Fill down the Employee field
- Fill down the Work Level field
- Reorder the data so that it is output in the same order as it comes in
- Output the data

Author: Kelly Gilbert
Created: 2022-09-30
Requirements:
  - input dataset:
      - Fill Down Input.csv
  - output dataset (for results check only):
      - No output dataset this week (output example is an image for visual comparison)
"""


import pandas as pd


# input the data
df = pd.read_csv(r'.\inputs\Fill Down Input.csv')


# fill down the employee and work level fields
df['Employee'] = df['Employee'].ffill()
df['Work Level'] = df['Work Level'].ffill().astype(int)


# output the file in Record ID order
( df.sort_values(by='Record ID')
    .to_csv(r'.\outputs\output-2022-39.csv', index=False) )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week
