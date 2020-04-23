# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-03
https://preppindata.blogspot.com/2020/01/2020-week-3.html
 
Summarizing NBA data

- For each team we're looking to discover the following information:
  Rank: Rank for each team within their conference.
  W: Wins for each team.
  L: Losses for each team.
  Pct: Win percentage for each team.
  Conf: The wins and losses for each team against teams within the same conference only.
  Home: The wins and losses for home games for each team.
  Away: The wins and losses for away games for each team.
  L10: The wins and losses for the last (most recently played) 10 games for each team.
  Strk: The current winning or losing streak that each team is on.
  The only column not required for this challenge is the GB (games behind).
- After producing these pieces of information, split the teams into two separate outputs - 
  one for each conference

Author: Kelly Gilbert
Created: 2020-02-15
Requirements: input dataset
  - PD - NBA Results.xlsx
"""


from datetime import datetime as dt
from numpy import where, nan
from os import chdir
from pandas import concat, DataFrame, ExcelFile, melt, rename


# import the data
chdir('C:\\projects\\preppin-data-challenge\\preppin-data-2020-03')
xl = ExcelFile(r'.\inputs\PD - NBA Results.xlsx')


# import the team info and correct spelling
df_team = xl.parse('Team List')
df_team.rename(columns = {'Divison':'Division'}, inplace = True)


# concatenate the results sheets
result_sheets = [s for s in xl.sheet_names if 'Results' in s]
df = None
for sheet in result_sheets:
    df = concat([df, xl.parse(sheet)])


# keep necessary columns, remove future games, identify winner/loser
df = df[['Date', 'Visitor/Neutral', 'PTS', 'Home/Neutral', 'PTS.1']]
df = df[df['PTS'].notna()]
df['winner'] = where(df['PTS']>=df['PTS.1'], df['Visitor/Neutral'], df['Home/Neutral'])
df['loser'] = where(df['PTS']>=df['PTS.1'], df['Home/Neutral'], df['Visitor/Neutral'])


# convert date
df['Date'] = [dt.strptime(d, '%a %b %d %Y') for d in df['Date']]


# add the conferences
df = df.merge(df_team, left_on='winner', right_on='Team', how='left') \
     .drop(columns=['Team','Division'])
df = df.merge(df_team, left_on='loser', right_on='Team', how='left', 
              suffixes=('_winner', '_loser')).drop(columns=['Team','Division'])
df['in_conference'] = where(df['Conference_winner']==df['Conference_loser'], 1, 0)


# put winner/loser into separate rows
df = melt(df, id_vars=['Date', 'Home/Neutral', 'Visitor/Neutral','in_conference'],  value_vars=['winner', 'loser'], 
          var_name='team_type', value_name='team')
df['home_flag'] = where(df['team']==df['Home/Neutral'], 1, 0)
df['visitor_flag'] = where(df['team']==df['Visitor/Neutral'], 1, 0)
df['win_flag'] = where(df['team_type']=='winner', 1, nan)
df['loss_flag'] = where(df['team_type']=='loser', 1, nan)



# calculate win/loss streak
# this will count up from one until it hits a NaN
df.sort_values(['team', 'Date'], ascending=False, inplace=True)
df['win_streak'] = df.groupby('team')['win_flag'].cumsum(skipna=False)
df['loss_streak'] = df.groupby('team')['loss_flag'].cumsum(skipna=False)

# flag if in last 10 games



# summarize
# by team,
# count win flag = W
# count loss flag = L
# count conf win
# count conf loss
# count home win
# count home loss
# count away win
# count away loss
# count l10 win
# count L10 loss
# count streak

# calc Pct = W / (W+L)
# assemble the win/loss strings
# rank within the conference

# reorder the fields and output the data 
  Rank: Rank for each team within their conference.
  W: Wins for each team.
  L: Losses for each team.
  Pct: Win percentage for each team.
  Conf: The wins and losses for each team against teams within the same conference only.
  Home: The wins and losses for home games for each team.
  Away: The wins and losses for away games for each team.
  L10: The wins and losses for the last (most recently played) 10 games for each team.
  Strk: The current winning or losing streak that each team is on.
  The only column not required for this challenge is the GB (games behind).
- After producing these pieces of information, split the teams into two separate outputs - 
  one for each conferenc











