# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-01
https://preppindata.blogspot.com/2020/01/2020-week-1.html
 
Reformat headings and add totals to financial data

Author: Kelly Gilbert
Created: 2020-01-11
Requirements: input dataset '\inputs\PD 2020 WK 1 Input - Sheet1.csv'
"""


import pandas as pd


# read in the file
df = pd.read_csv('.\\inputs\\PD 2020 WK 1 Input - Sheet1.csv')

# replace nulls with zeroes
df['Profit'].fillna(0, inplace=True)

# extract the hierarchy from the Item and copy it
df['Hierarchy'] = df['Item'].str.extract('([\d\.]+?)\.? .*')
df['Hierarchy2'] = df['Hierarchy']
df['Level'] = df['Hierarchy'].str.count('\.')
maxLevel = df['Level'].max()

# iterate through the hierarchy levels, creating subtotals at each level
dfSubtotal = None
for i in range(maxLevel, 0, -1):
    # remove a layer of hierarchy
    df['Hierarchy2'] = df['Hierarchy2'].str.extract('(.*?)\.\d+$')
   
    # using only the detail records, sum by current level of hierarchy
    # and add to the Subtotal df
    dfSubtotal = pd.concat([dfSubtotal, 
      df[df['Level']==maxLevel].groupby(df['Hierarchy2'], as_index=True)['Profit'].sum()])
  
# join subtotals back to the main dataframe and update the Profit
df = pd.merge(df, dfSubtotal, how='left', left_on='Hierarchy', right_index=True)
df['Profit'] = df['Profit_x'] + df['Profit_y'].fillna(0)

# add the spacing to the Item
df['Item'] = [' '* 5*x for x in df['Level']] + df['Item']

# clean up columns
df = df[['Item','Profit']]

# output the file
df.to_csv(path_or_buf='.\\outputs\\output-2020-01.csv', index=False)