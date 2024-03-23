# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 11 - 13 months in a year (Polars)
https://preppindata.blogspot.com/2024/03/2024-week-11-13-months-in-year.html

- Input the data
- Create a row for each day of the year
  - I've chosen to use 2024 for the challenge so results will be different if you select a 
    non-leap year
- Calculate the new months of the year such that the first 28 days of the month are month 1, the 
  next 28 days are month 2, etc
  - This will give you 14 months, with the 14th month containing just 2 days
- Create a new date with the format:
  - New day of the month / New month / 2024
  - e.g. 20/11/2024 becomes 17/12/2024
- Filter the data to only contain dates for which the month has changed in the new system
- Output the data

Author: Kelly Gilbert
Created: 2024-03-19
Requirements:
  - input dataset:
      - 2024W11 Input.csv
  - output dataset (for results check only):
      - 2024W11 Output.csv
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

YEAR = 2024


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# convert the input dates to date
df_in = ( pl.read_csv(r'.\inputs\2024W11 Input.csv',n_rows=2, try_parse_dates=True)
            .select(
                (pl.col('Date') + f' {YEAR}')
                    .str.replace('st|nd|rd|th', '')
                    .str.to_date('%d %B %Y')
            )
        )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df = ( pl.LazyFrame({ 'Date' : pl.date_range(df_in[0, 0],
                                   df_in[1, 0],
                                   interval='1d',
                                   eager=True) })
         .with_columns( 
             ((pl.col('Date').dt.ordinal_day() - 1) // 28 + 1).alias('new_month'),
             ((pl.col('Date').dt.ordinal_day() - 1) % 28 + 1).alias('new_day')
         )
         .with_columns(
             (pl.col('new_day').cast(pl.Utf8).str.zfill(2) + '/' 
                   + pl.col('new_month').cast(pl.Utf8).str.zfill(2) + '/'
                   + pl.lit(YEAR).cast(pl.Utf8)).alias('New Date')
         )
     )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# output only the changed months
( df
      .filter(pl.col('new_month') != pl.col('Date').dt.month())
      .select(pl.col('Date'), pl.col('New Date'))
      .collect()
      .write_csv(r'.\outputs\output-2024-11.csv',
                 date_format = '%d/%m/%Y') 
)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2024W11 Output.csv']
my_files = [r'.\outputs\output-2024-11.csv']
unique_cols = [['Date']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
