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
from pandas import concat, ExcelFile, ExcelWriter, melt

# import the data
chdir('C:\\projects\\preppin-data-challenge\\preppin-data-2020-03')
xl = ExcelFile(r'.\inputs\PD - NBA Results.xlsx')


# import the team info and correct spelling of Division
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
id_vars = ['Date', 'Home/Neutral', 'Visitor/Neutral', 
           'Conference_winner', 'Conference_loser', 'in_conference']
df = melt(df, id_vars=id_vars,  value_vars=['winner', 'loser'], 
          var_name='team_type', value_name='Team')
df['conference'] = where(df['team_type']=='winner', df['Conference_winner'], df['Conference_loser'])
df.drop(columns=['Conference_winner', 'Conference_loser'], inplace=True)


# flags for summarization
df['home_flag'] = where(df['Team']==df['Home/Neutral'], 1, 0)
df['away_flag'] = where(df['Team']==df['Visitor/Neutral'], 1, 0)

df['win_flag'] = where(df['team_type']=='winner', 1, nan)
df['loss_flag'] = where(df['team_type']=='loser', 1, nan)

df.sort_values(['Team', 'Date'], ascending=False, inplace=True)
df['win_streak'] = df.groupby('Team')['win_flag'].cumsum(skipna=False) # this will count up from one until it hits a NaN
df['loss_streak'] = df.groupby('Team')['loss_flag'].cumsum(skipna=False)

df['win_flag'] = df['win_flag'].fillna(0)
df['loss_flag'] = df['loss_flag'].fillna(0)

df['conference_win_flag'] = where((df['team_type']=='winner') & (df['in_conference']==1), 1, 0)
df['conference_loss_flag'] = where((df['team_type']=='loser') & (df['in_conference']==1), 1, 0)

df['home_win_flag'] = where((df['team_type']=='winner') & (df['home_flag']==1), 1, 0)
df['home_loss_flag'] = where((df['team_type']=='loser') & (df['home_flag']==1), 1, 0)

df['away_win_flag'] = where((df['team_type']=='winner') & (df['away_flag']==1), 1, 0)
df['away_loss_flag'] = where((df['team_type']=='loser') & (df['away_flag']==1), 1, 0)

df['date_rank'] = df.groupby('Team')['Date'].rank(method='first', ascending=False)
df['L10_win_flag'] = where((df['team_type']=='winner') & (df['date_rank']<=10), 1, 0)
df['L10_loss_flag'] = where((df['team_type']=='loser') & (df['date_rank']<=10), 1, 0)


# summarize by team
df_summary = df.groupby(['conference','Team'], as_index=False).agg( 
               { 'win_flag' : {'W' : 'sum'},
                 'loss_flag' : {'L' : 'sum'},
                 'conference_win_flag' : {'Conf_W' : 'sum'},
                 'conference_loss_flag' : {'Conf_L' : 'sum'},
                 'home_win_flag' : {'Home_W' : 'sum'},
                 'home_loss_flag' : {'Home_L' : 'sum'},
                 'away_win_flag' : {'Away_W' : 'sum'},
                 'away_loss_flag' : {'Away_L' : 'sum'},
                 'L10_win_flag' : {'L10_W' : 'sum'},
                 'L10_loss_flag' : {'L10_L' : 'sum'},
                 'win_streak' : {'Strk_W' : 'max'},
                 'loss_streak' : {'Strk_L' : 'max'}
               }
             )

# remove the extra column index level and convert numbers to integer
df_summary.columns = [c[0] if c[1]=='' else c[1] for c in df_summary.columns]
df_summary = concat([df_summary[['conference','Team']], 
                     df_summary.iloc[:, 2:].fillna(0).astype(int)], axis=1)


# calculations
df_summary['Pct'] = (df_summary['W'] / (df_summary['W'] + df_summary['L'])).round(3)
df_summary['Conf'] = df_summary['Conf_W'].astype(str) + '-' + df_summary['Conf_L'].astype(str)
df_summary['Home'] = df_summary['Home_W'].astype(str) + '-' + df_summary['Home_L'].astype(str)
df_summary['Away'] = df_summary['Away_W'].astype(str) + '-' + df_summary['Away_L'].astype(str)
df_summary['L10'] = df_summary['L10_W'].astype(str) + '-' + df_summary['L10_L'].astype(str)
df_summary['Strk'] = where(df_summary['Strk_W']==0, 'L' + df_summary['Strk_L'].astype(str), 
                                                    'W' + df_summary['Strk_W'].astype(str))

# conference rank
df_summary['Rank'] = df_summary.groupby('conference')['Pct'].rank(method='max', ascending=False)
df_summary.sort_values(['conference', 'Rank'], ascending=True, inplace=True)
    # the provided output isn't sorted

# output one sheet per conference
cols = ['Rank', 'Team', 'W', 'L', 'Pct', 'Conf', 'Home', 'Away', 'L10', 'Strk']
writer = ExcelWriter(r'.\outputs\output-2020-03.xlsx', engine='xlsxwriter')

for c in df_summary['conference'].unique():
    df_summary[df_summary['conference']==c].to_excel(writer, columns=cols,  
                                                     sheet_name=c + 'ConferenceStandings', 
                                                     index = False)
writer.save()


# check results
#...
