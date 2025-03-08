# -*- coding: utf-8 -*-
"""
Preppin' Data 2025: Week 52 - Naughty or Nice
https://preppindata.blogspot.com/2024/12/2024-week-52-naughty-or-nice.html

- Input the data
- Split the File Paths to determine which list each record is on
- Create an Index field combing the File Path number and id (id 7 from Naughty 1 file should create an id of 1007) 
- Create a count of how many naughty listings and nice listings each name has
- Determine what list each person should be on
  - If the listings are tied, find the latest listing for those people as that will determine which listing they are on
- Remove any unnecessary fields and create one row per person:
  - Leaves Name and 'Naughty or Nice' field
- Output the data

Author: Kelly Gilbert
Created: 2025-03-05
Requirements:
  - input dataset:
      - PD 2024 Wk 52 Input.csv
  - output dataset (for results check only):
      - N/A - checked by visual inspection
"""


import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\PD 2024 Wk 52 Input.csv')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df[['list', 'order']] = df['File Paths'].str.extract(r'(.*?) (\d+)')

df_out = ( 
    df
        .assign(order = df['order'].astype(int))
        .assign(index = lambda df_x: df_x['order'] * 100000 + df_x['id'])
        .groupby(['first_name', 'list'], as_index=False)
        .agg(count = ('id', 'count'),
             max_id = ('id', 'max'))
        .sort_values(['count', 'max_id'], ascending=False)
        .drop_duplicates('first_name')
        .rename(columns={'first_name' : 'Name',
                         'list' : 'Naughty or Nice'})
        [['Name', 'Naughty or Nice']]
)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2024-52.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection of screenshot
