# -*- coding: utf-8 -*-
"""
Preppin' Data 2025: Week 52 - Naughty or Nice (polars)
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


import polars as pl


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pl.scan_csv(r'.\inputs\PD 2024 Wk 52 Input.csv')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df_out = ( 
    df
        # split the file path into columns
        .with_columns(
            pl.col('File Paths')
                .str.split(' ')
                .list.to_struct(n_field_strategy='max_width', fields=['list', 'order'])
        )
        .unnest('File Paths')
        .with_columns( 
            pl.col('order').cast(pl.Int8)
        )

        # identify the list by person
        .with_columns( 
            pl.col('order') * 100000 + pl.col('id').alias('index')
        )
        .group_by([pl.col('first_name'), pl.col('list')])
        .agg(
            pl.col('id').count().alias('count'),
            pl.col('id').max().alias('max_id')
        )
        .sort(
            [
                pl.col('first_name'), 
                pl.col('count'), 
                pl.col('max_id')
            ], 
            descending=True
        )
        .unique('first_name')

        # clean up cols
        .select(
            pl.col('first_name').alias('Name'), 
            pl.col('list').alias('Naughty or Nice')
        )
)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.collect().write_csv(r'.\outputs\output-2024-52.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection of screenshot
