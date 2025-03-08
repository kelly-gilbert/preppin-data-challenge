# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 51 - Strictly Positive Improvements? (polars)
https://preppindata.blogspot.com/2024/12/2024-week-51-strictly-positive.html

- Input the data
- The webscraping isn't quite perfect and the table headers are repeated throughout the dataset, 
  make sure these are removed
- Make sure that the Week field is numeric
- The Score field is made up of the Total Score and individual judges scores
  - Create a field for the total score
  - Count how many judges there were 
  - Create an Avg Judge's Score field
    - i.e. Total Score/Number of Judges
- Since we're interested in couple's improvement from the start of the series and the end of the series, 
  we only need to retain rows relating to the couple's first dance (which may not have been in week 1) 
  and their dances in the final
  - This means we're only interested in couples who made it to the final
- Couples dance multiple times in the final. Take the average of their Avg Judge's Score
- Find the Percentage difference between their Avg Judge's Score for their first dance and the average 
  for their dances in the final
- The final output should contain a row for each couple, with their Percentage difference and only the 
  Avg Judge's Score in the final, along with the Result
  - i.e. whether they won, were a runner-up or came third
- Output the data

Author: Kelly Gilbert
Created: 2024-03-07
Requirements:
  - input dataset:
      - strictly_come_dancing_series_1_to_21_tables.csv
  - output dataset (for results check only):
      - 2024W51 Output.csv
"""

import numpy as np
import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = (
    pl.scan_csv(r'.\inputs\strictly_come_dancing_series_1_to_21_tables.csv')
        # remove extra header rows
        .filter(pl.col('Couple') != 'Couple')

        # extract numeric week and scores, calculate average, find first week by couple
        .with_columns(
            pl.col('Week')
                .str.extract(r'Week (\d+)')
                .cast(pl.Int8)
                .alias('week_nbr'),
            pl.col('Week')
                .str.contains('Final')
                .alias('is_final'),
            pl.col('Scores')
                .str.extract(r'(\d+)')
                .cast(pl.Int8)
                .alias('total_score'),
            (pl.col('Scores')
                .str.count_matches(r'\,') + 1)
                .alias('num_judges')
        )
        .with_columns( 
            (pl.col('total_score') / pl.col('num_judges'))
                .alias('avg_score'),
            pl.col('week_nbr')
                .min()
                .over([pl.col('Series'), pl.col('Couple')])
                .alias('first_week')
        )
)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df_first_week = (
    df
        .filter(pl.col('week_nbr') == pl.col('first_week'))
        .group_by(
            [pl.col('Series'), pl.col('Couple'), pl.col('week_nbr')],
        )
        .agg(pl.col('avg_score').mean())
)

df_final_week = ( 
    df
        .filter(pl.col('is_final') & (pl.col('Result').fill_null('') != 'Eliminated'))
        .with_columns(
            pl.when(pl.col('Result').is_in(['Safe', 'Eliminated']) | pl.col('Result').is_null())
            .then(pl.lit(''))
            .otherwise(pl.col('Result'))
            .alias('result_adj')
        )
        .group_by([pl.col('Series'), pl.col('Couple')])
        .agg(
            pl.col('avg_score').mean(),
            pl.col('result_adj').max()
        )
)


# find the % change from first week to final
df_out = (
    df_first_week
        .join(
            df_final_week,
            on=[pl.col('Series'), pl.col('Couple')],
            how='inner',
            suffix='_final'
        )
        .with_columns(
            (pl.col('avg_score_final') / pl.col('avg_score') - 1).alias('% Change')
        )
        .select([ 
            pl.col('Series'),
            pl.col('Couple'),
            pl.col('result_adj').alias('Finalist Positions'),
            pl.col('avg_score_final').alias("Avg Judge's Score"),
            pl.col('% Change')
        ])
)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.collect().write_csv(r'.\outputs\output-2024-51.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2024W51 Output.csv']
my_files = [r'.\outputs\output-2024-51.csv']
unique_cols = [['Series', 'Couple']]
col_order_matters = False
round_dec = 6

output_check(
    solution_files=solution_files, 
    my_files=my_files, 
    unique_cols=unique_cols, 
    col_order_matters=col_order_matters, 
    round_dec=round_dec
)
