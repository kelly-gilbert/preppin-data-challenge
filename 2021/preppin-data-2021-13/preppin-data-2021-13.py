# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 13 - Premier League Statistics
https://preppindata.blogspot.com/2021/03/2021-week-13.html

- Input all the files
- Remove all goalkeepers from the data set
- Remove all records where appearances = 0
- In this challenge we are interested in the goals scored from open play
    - Create a new “Open Play Goals” field (the goals scored from open play is the number of goals
      scored that weren’t penalties or freekicks)
    - Note some players will have scored free kicks or penalties with their left or right foot
    - Be careful how Prep handles null fields! (have a look at those penalty and free kick fields)
    - Rename the original Goals scored field to Total Goals Scored
- Calculate the totals for each of the key metrics across the whole time period for each player,
  (be careful not to lose their position)
- Create an open play goals per appearance field across the whole time period
- Rank the players for the amount of open play goals scored across the whole time period, we are
  only interested in the top 20 (including those that are tied for position) – Output 1
- Rank the players for the amount of open play goals scored across the whole time period by
  position, we are only interested in the top 20 (including those that are tied for position) –
  Output 2
- Output the data – in your solution on twitter / the forums, state the name of the player who was
  the only non-forward to make it into the overall top 20 for open play goals scored

Author: Kelly Gilbert
Created: 2021-05-06
Requirements:
  - input datasets (pl_xx-yy.csv files for each season)
  - output datasets (for results check):
    - Rank by Position.csv
    - Overall Rank.csv
"""


from os import listdir
from pandas import concat, read_csv


# --------------------------------------------------------------------------------------------------
# input data
# --------------------------------------------------------------------------------------------------

df = concat([read_csv(r'.\inputs\\' + f) for f in listdir(r'.\inputs')])
#df.info(verbose=True)    # investigate the list of fields


# --------------------------------------------------------------------------------------------------
# prep data
# --------------------------------------------------------------------------------------------------

# remove the space after the player name
df['Name'] = df['Name'].str.strip()

# remove all goalkeepers and appearances = 0
#df['Position'].unique()    # review the positions in the dataset
df = df.loc[(df['Position'] != 'Goalkeeper') & (df['Appearances'] != 0)]

# calculate Open Play Goals
df['Open Play Goals'] = (df['Goals'] - df['Penalties scored'].fillna(0) \
                                     - df['Freekicks scored'].fillna(0)).astype(int)

# rename the original Goals field to Total Goals Scored
df.rename(columns={'Goals' : 'Total Goals'}, inplace=True)

# check for players with multiple positions
df.groupby(['Name', 'Position']).size().reset_index()\
  .groupby('Name').size().reset_index().sort_values(by=0, ascending=False)

# calculate totals for each key metric for each player
df_sum = df.groupby(['Name', 'Position'])[['Appearances', 'Open Play Goals',
                                           'Goals with right foot', 'Goals with left foot',
                                           'Total Goals', 'Headed goals']]\
                                         .sum().reset_index()

# create an open play goals per appearance field
df_sum['Open Play Goals/Game'] = round(df_sum['Open Play Goals'] /
                                       df_sum['Appearances'], 9).astype(float)

# rank the players for the amount of open play goals scored and keep the top 20 by position
df_sum['Rank by Position'] = df_sum.groupby('Position')['Open Play Goals']\
                                   .rank(method='min', ascending=False).astype(int)

# rank the players for the amount of open play goals scored and keep the top 20 overall
df_sum['Rank'] = df_sum['Open Play Goals'].rank(method='min', ascending=False).astype(int)


# --------------------------------------------------------------------------------------------------
# output data
# --------------------------------------------------------------------------------------------------

# output #1 - rank by position
out_cols = ['Rank by Position', 'Open Play Goals', 'Goals with right foot', 'Goals with left foot',
            'Position', 'Appearances', 'Total Goals', 'Open Play Goals/Game', 'Headed goals',
            'Name']

df_sum[df_sum['Rank by Position'] <= 20].sort_values(by=['Position', 'Rank by Position'])\
    .to_csv(r'.\outputs\output-2020-13-rank-by-position.csv', index=False, columns=out_cols)


# output #2 - overall rank
out_cols = ['Open Play Goals', 'Goals with right foot', 'Goals with left foot',
            'Position', 'Appearances', 'Rank', 'Total Goals', 'Open Play Goals/Game',
            'Headed goals', 'Name']

df_sum[df_sum['Rank'] <= 20].sort_values(by='Rank')\
    .to_csv(r'.\outputs\output-2020-13-overall-rank.csv', index=False, columns=out_cols)


# name of the player who was the only non-forward in the top 20 for open play goals scored
df_sum[(df_sum['Position'] != 'Forward') & (df_sum['Rank'] <= 20)]


# --------------------------------------------------------------------------------------------------
# check results
# --------------------------------------------------------------------------------------------------

solutionFiles = ['Rank by Position.csv', 'Overall Rank.csv']
myFiles = ['output-2020-13-rank-by-position.csv', 'output-2020-13-overall-rank.csv']
col_order_matters = True


for i in range(len(solutionFiles)):
    print('\n---------- Checking \'' + myFiles[i] + '\' ----------\n')

    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solutionFiles[i])
    dfMine = read_csv('.\\outputs\\' + myFiles[i])

    # are the fields the same and in the same order?
    solutionCols = list(dfSolution.columns)
    myCols = list(dfMine.columns)
    if not col_order_matters:
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

        if len(dfCompare[dfCompare['in_solution'].isna() | dfCompare['in_mine'].isna()]) > 0:
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')

    print('\n')
