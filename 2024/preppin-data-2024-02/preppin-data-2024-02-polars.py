# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 02 - Average Price Analysis (polars)
https://preppindata.blogspot.com/2024/01/2024-week-2-average-price-analysis.html

- Input the two csv files
- Union the files together
- Convert the Date field to a Quarter Number instead
  - Name this field Quarter
- Aggregate the data in the following ways:
  - Median price per Quarter, Flow Card? and Class
  - Minimum price per Quarter, Flow Card? and Class
  - Maximum price per Quarter, Flow Card? and Class
- Create three separate flows where you have only one of the aggregated measures in each. 
  - One for the minimum price
  - One for the median price
  - One for the maximum price
- Now pivot the data to have a column per class for each quarter and whether the passenger had a 
  flow card or not
- Union these flows back together

What's this you see??? Economy is the most expensive seats and first class is the cheapest? When you 
go and check with your manager you realise the original data has been incorrectly classified so you 
need to the names of these columns.
- Change the name of the following columns:
  - Economy to First
  - First Class to Economy
  - Business Class to Premium
  - Premium Economy to Business
- Output the data

Author: Kelly Gilbert
Created: 2024-MM-DD
Requirements:
  - input datasets:
      - PD 2024 Wk 1 Output Flow Card.csv
      - PD 2024 Wk 1 Output Non-Flow Card.csv
  - output dataset (for results check only):
      - PD 2024 Wk 2 Output.csv
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

REPLACE_CLASS = { 'First Class' : 'Economy',
                  'Economy' : 'First',
                  'Business Class' : 'Premium',
                  'Premium Economy' : 'Business' }


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

grouping_cols = ['Flow Card?', 'Quarter', 'Class']

df = ( pl.scan_csv(r'.\inputs\*.csv', 
                   try_parse_dates=True)
         
         # add the quarter
         .with_columns(pl.col('Date').dt.quarter().alias('Quarter'))
         
         # aggregate price
         .group_by(grouping_cols)
         .agg(
              pl.col('Price').min().alias('Minimum Price'),
              pl.col('Price').max().alias('Maximum Price'),
              pl.col('Price').median().alias('Median Price')
         )
         
         # fix class names
         .with_columns( 
             pl.col('Class').map_dict(REPLACE_CLASS, default=pl.col('Class'))
         )
         
         # reshape
         .melt(id_vars=grouping_cols, 
               value_vars=['Minimum Price', 'Maximum Price', 'Median Price'],
               variable_name='Metric Name')
         .group_by(grouping_cols[:-1] + ['Metric Name'])
         .agg([
             pl.col('value').filter(pl.col('Class')==c).first().alias(c)
             for c in REPLACE_CLASS.values()
             ])
     )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

( df.collect()
    .write_csv(r'.\outputs\output-2024-02.csv')
)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# remove the Metric Name column for checking
( df.collect() 
    .drop(columns='Metric Name')
    .write_csv(r'.\outputs\output-2024-02_check.csv')
)


# compare the files
solution_files = [r'.\outputs\PD 2024 Wk 2 Output.csv']
my_files = [r'.\outputs\output-2024-02_check.csv']
unique_cols = [['Flow Card?', 'Quarter', 'Economy', 'Premium', 'Business', 'First']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
