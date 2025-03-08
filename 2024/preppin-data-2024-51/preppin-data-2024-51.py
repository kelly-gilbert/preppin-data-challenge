# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 51 - Strictly Positive Improvements?
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
Created: 2024-03-05
Requirements:
  - input dataset:
      - strictly_come_dancing_series_1_to_21_tables.csv
  - output dataset (for results check only):
      - 2024W51 Output.csv
"""

import numpy as np
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = (
    pd.read_csv(r'.\inputs\strictly_come_dancing_series_1_to_21_tables.csv')
        .query("Couple != 'Couple'")    # remove extra header rows
)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# extract numeric week and scores
df['week_nbr'] = df['Week'].str.extract(r'Week (\d+)').astype(int)

df[['total_score', 'score_list']] = df['Scores'].str.extract(r'(\d+) *\(?([\d\, ]+)?\)?')
df['total_score'] = df['total_score'].astype(float)
df['num_judges'] = df['score_list'].str.count(',') + 1
df['avg_score'] = df['total_score'] / df['num_judges']


# keep the first week per couple and the final week of each series; average the final scores if there are multiple
ignore_result = ['Safe', 'Eliminated']

df_first_week = (
    df
        [df['week_nbr'] == df.groupby(['Series', 'Couple'])['week_nbr'].transform('min')]
        .groupby(
            ['Series', 'Couple', 'week_nbr'],
            as_index=False)
        ['avg_score'].mean()         
)

df_final_week = ( 
    df
        [df['Week'].str.contains(r'Final') & (df['Result'] != 'Eliminated')]
        .assign(
            result_adj = \
                lambda df_x: np.where(df_x['Result'].isin(ignore_result) | df_x['Result'].isna(),
                                      '',
                                      df_x['Result'])
        )
        .groupby(['Series', 'Couple', 'week_nbr'], 
                 as_index=False
        )
        .agg(
            avg_score = ('avg_score', 'mean'),
            result_adj = ('result_adj', 'max')
        )
)


# find the % change from first week to final
df_out = (
    df_first_week
        .merge(
            df_final_week,
            on=['Series', 'Couple'],
            how='inner',
            suffixes=['_first', '_final']
        ) 
        .assign(pct_change = lambda df_x: df_x['avg_score_final'] / df_x['avg_score_first'] - 1)
        [['Series', 'Couple', 'result_adj', 'avg_score_final', 'pct_change']]
        .rename(
            columns={ 'result_adj' : 'Finalist Positions',
                      'avg_score_final' : "Avg Judge's Score",
                      'pct_change' : '% Change' }
        )
)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2024-51.csv', index=False)


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
