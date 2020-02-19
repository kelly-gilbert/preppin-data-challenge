# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-05
https://preppindata.blogspot.com/2020/01/2020-week-5.html
 
- Input the data
- Remove the games that have null scores at halftime
- Determine the Standard Competition rank based on Diff (ie margin of victory - the larger the better)
- Using that rank give three statistics per rank:
  - Best game Rank per Venue
  - Worst game Rank per Venue
  - Average Rank per Venue
  - Number of Games played at that venue
- Output the data

Author: Kelly Gilbert
Created: 2020-02-18

Requirements:
  - input dataset: PD 2020 Wk 5 Input.csv

"""

from pandas import read_csv


# import the data
df = read_csv(r'.\inputs\PD 2020 Wk 5 Input.csv')


# remove games with null ('-') scores at halftime
df = df[(df['HTf'] != '-') & (df['HTa'] != '-')]


# determine standard competition rank based on Diff (larger = better)
df['Rank'] = df['Diff'].rank(method='min', ascending=False)


# summarize by venue (count of games, best rank, worst rank, avg rank)
df_sum = df.groupby(['Venue'], as_index=False).agg( 
                 { 'Rank' : [('Count', 'count'),
                             ('Best','min'),
                             ('Worst', 'max'),
                             ('Average', 'mean')]
                 }
               )
df_sum.columns = ['Venue', 
                  'Number of Game',
                  'Best Rank (Standard Competition)', 
                  'Worst Rank (Standard Competition)', 
                  'Avg. Rank (Standard Competition)']

df_sum[['Venue', 'Avg. Rank (Standard Competition)']].sort_values(by=['Venue'])


# output the file
df_sum.to_csv(path_or_buf=r'.\outputs\output-2020-05.csv', index=False)