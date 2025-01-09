# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 35 - Premier League Results
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


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\Premier League Results 2023_24.xlsx') as xl:
    df = pd.read_excel(xl, header=None)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# add the row number
df['Source Row Number'] = df.index


# extract the match day
df['Matchday'] = df[0].str.extract(r'Matchday (\d+) ' ).ffill()


# put data into 1 column and remove non-game records
df_out = ( 
      df
          .melt(id_vars=['Source Row Number', 'Matchday'], value_vars=[0, 1])
          .query("value.str.startswith('FT', na=False)") 
)


# replace newlines with delimiter and split columns
df_out[['Date', 'Home Score', 'Home Team', 'Away Score', 'Away Team']] = ( 
    df_out['value']
        .str.replace(r'Match .*?\n+\s* *', '', regex=True)
        .str.split(r'\n+\s*', expand=True)
        .drop(columns=[0, 4, 7])
)


# date to datetime
df_out['Date'] = pd.to_datetime(df_out['Date'].str.replace('Sept', 'Sep'), format='%d %b %y')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

( df_out
     .drop(columns=['variable', 'value'])
     .to_csv(r'.\outputs\output-2024-35.csv', index=False, date_format='%d/%m/%Y')
)


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
