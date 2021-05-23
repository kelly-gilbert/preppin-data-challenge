# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 16 - The Super League
https://preppindata.blogspot.com/2021/04/2021-week-16-super-league.html

- Input the data
- Calculate the Total Points for each team. The points are as follows:
  Win - 3 Points
  Draw - 1 Point
  Lose - 0 Points
- Calculate the goal difference for each team. Goal difference is the difference between goals
  scored and goals conceded.
- Calculate the current rank/position of each team. This is based on Total Points (high to low) and
  in a case of a tie then Goal Difference (high to low).
- The current league table is our first output.
- Assuming that the 'Big 6' didn't play any games this season, recalculate the league table.
- After removing the 6 clubs, how has the position changed for the remaining clubs?
- The updated league table is the second output.
- Bonus - Think about features in Tableau Prep to make this repeatable process easier!

Author: Kelly Gilbert
Created: 2021-05-09
Requirements:
  - input dataset:
      - PL Fixtures.csv
  - output dataset (for results check):
      - Preppin Data 2020W9 Output.csv

"""


from numpy import where
from pandas import concat, melt, read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\inputs\PL Fixtures.csv', parse_dates=['Date'], dayfirst=True)\
     .dropna(subset=['Result'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# identify games involving the big 6
# sorted(concat([df['Home Team'], df['Away Team']]).unique())
big_6 = ['Arsenal', 'Chelsea', 'Liverpool', 'Man Utd', 'Man City', 'Spurs']

df['big_6'] = where(df['Home Team'].isin(big_6) | df['Away Team'].isin(big_6), 1, 0)

# split the score into away and home
df[['Home Score', 'Away Score']] = df['Result'].str.split(' - ', expand=True).astype(int)
df['Winner'] = where(df['Away Score'] == df['Home Score'], 'Draw',
                 where(df['Away Score'] > df['Home Score'], 'Away', 'Home'))

# stack the teams
value_vars = ['Home Team', 'Away Team']
df_m = df.melt(id_vars=[c for c in df.columns if c not in value_vars], value_name='Team')


# calculate the goals scored/conceded and total points for ech team
df_m['Goals Scored'] = where(df_m['variable'] == 'Home Team', df_m['Home Score'],
                             df_m['Away Score'])

df_m['Goals Conceded'] = where(df_m['variable'] == 'Home Team', df_m['Away Score'],
                               df_m['Home Score'])

df_m['Total Points'] = where(df_m['Goals Scored'] == df_m['Goals Conceded'], 1,
                         where(df_m['Goals Scored'] > df_m['Goals Conceded'], 3, 0))

df_m['Goal Difference'] = df_m['Goals Scored'] - df_m['Goals Conceded']

df_m['Total Games Played'] = 1    # counter


# calculate the total points for each team (full data)
sum_cols = ['Total Games Played', 'Total Points', 'Goal Difference']

total_1 = df_m.groupby('Team')[sum_cols].sum().reset_index()
total_2 = df_m[df_m['big_6'] == 0].groupby('Team')[sum_cols].sum().reset_index()


# calculate the current rank/position of each team. This is based on Total Points (high to low) and
# in a case of a tie then Goal Difference (high to low).
cols = ['Total Points', 'Goal Difference']

total_1['Position'] = total_1[cols].apply(tuple, axis=1)\
                                   .rank(method='min', ascending=False).astype(int)
total_2['Position'] = total_2[cols].apply(tuple, axis=1)\
                                   .rank(method='min', ascending=False).astype(int)


# find the change in position
total_2 = total_2.merge(total_1[['Team', 'Position']], on='Team', how='left', suffixes=['', '_1'])
total_2['Position Change'] = total_2['Position_1'] - total_2['Position']
total_2.drop(columns=['Position_1'], inplace=True)


#---------------------------------------------------------------------------------------------------
# output the files
#---------------------------------------------------------------------------------------------------

total_1.to_csv('.\\outputs\\output-2021-16-current-table.csv', index=False,
               columns=['Position', 'Team', 'Total Games Played', 'Total Points', 'Goal Difference'])
total_2.to_csv('.\\outputs\\output-2021-16-updated-table.csv', index=False,
               columns=['Position Change', 'Position', 'Team', 'Total Games Played',
                        'Total Points', 'Goal Difference'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solutionFiles = ['Current Table.csv', 'Updated Table.csv']
myFiles = ['output-2021-16-current-table.csv', 'output-2021-16-updated-table.csv']
col_order_matters = False

for i in range(len(solutionFiles)):
    print('---------- Checking \'' + solutionFiles[i] + '\' ----------\n')

    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solutionFiles[i])
    dfMine = read_csv('.\\outputs\\' + myFiles[i])

    # week 16 only - fix trailing space in Position field
    dfSolution.columns = [c.strip() for c in dfSolution.columns]

    # are the fields the same and in the same order?
    solutionCols = list(dfSolution.columns)
    myCols = list(dfMine.columns)
    if col_order_matters == False:
         solutionCols.sort()
         myCols.sort()


    col_match = False
    if solutionCols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(dfSolution.columns)))
        print('    Columns in mine    : ' + str(list(dfMine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        dfSolution['join'] = 1
        dfMine['join'] = 1
        dfCompare = dfSolution.merge(dfMine, how='outer', on=list(dfSolution.columns)[:-1])
        dfCompare.rename(columns={'join_x':'in_solution', 'join_y':'in_mine'}, inplace=True)

        if dfCompare['in_solution'].count() != len(dfCompare):
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')

    print('\n')
