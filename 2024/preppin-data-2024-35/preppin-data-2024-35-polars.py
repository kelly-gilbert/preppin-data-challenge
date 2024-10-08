# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 35 - Premier League Results (polars)
https://preppindata.blogspot.com/2024/08/2024-week-35-premier-league-results.html

- Input the dataset
- Add in a row number as at source (this will help for next week's challenge)
- Create a column to show which Matchday (ie which game in the 38 game season) eachgame occured in
- Remove any rows of the data set that don't contain game information
- It's helpful to put all the match information in one column rather than the two columns inthe input
- Replace the new row character (\n) with a different character(s) (I use two pipecharacters: ||)
  - \n is recognised as char(10) by Prep Builder
- Form separate columns for:
  - Date
  - Home Score
  - Home Team
  - Away Score
  - Away Team
- Output the results

Author: Kelly Gilbert
Created: 2024-10-04
Requirements:
  - input dataset:
      - Premier League Results 2023_24.xlsx
  - output dataset (for results check only):
      - PD 2024 Wk 35 Output.csv
"""


import polars as pl
import polars.selectors as cs
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pl.read_excel(r'.\inputs\Premier League Results 2023_24.xlsx', has_header=False)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# add the row number
df_out = (( 
    df 
        # add row number
        .with_row_index(name='Source Row Number')
        
        # extract matchday
        .with_columns( 
            pl.col('column_1')
                .str.extract(r'Matchday (\d+) ')
                .fill_null(strategy='forward')
                .alias('Matchday')
        )
        
        # parse game info columns
        .unpivot(
            index=['Source Row Number', 'Matchday'], 
            on=['column_1', 'column_2']
        )
        .filter(pl.col('value').str.starts_with('FT'))
        .with_columns( 
            pl.col('value')
                .str.replace(r'Match .*?\n+\s*', '') 
                .str.extract_all(r'(.*?)\n+\s*')
                .list.eval(pl.element().str.strip_chars())
                .list.to_struct(fields=['_', 'Date', 'Home Score', 'Home Team', '_1', 'Away Score', 'Away Team', '_2'])
                .alias('split_fields')
        )
    )
    .unnest('split_fields')
    .select(~cs.starts_with(r'_') & ~cs.by_name(['variable', 'value']))   
    
    #
    .with_columns( 
        pl.col('Date')
            .str.replace('Sept', 'Sep')
            .str.to_date('%d %b %y')
    )
)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.write_csv(r'.\outputs\output-2024-35.csv', date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2024 Wk 35 Output.csv']
my_files = [r'.\outputs\output-2024-35.csv']
unique_cols = [['Date', 'Away Team', 'Home Team']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
