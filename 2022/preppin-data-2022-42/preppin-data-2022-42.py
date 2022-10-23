# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 42 - Missing Training Data
https://preppindata.blogspot.com/2022/10/2022-week-42-missing-training-data.html

- Input the data
- For each player and each session, we want to know what the date is of the next session
  - E.g. for Player 1 who had an Agility session on 4th Jan, their next Agility session 
    was 6th Jan - so we have missing data on 5th Jan
- For the most recent training session in the dataset, assign the next session as the maximum date 
  in the dataset
- Scaffold the data so we have a row for each player and each session
  - Careful of duplicates!
- Create a flag to indicate whether the score comes from an actual session, or is carried over 
  from the previous session
- Exclude all weekends (Saturdays & Sundays) from the dataset
  - Players need time off too!
- Output the data

Author: Kelly Gilbert
Created: 2022-10-20
Requirements:
  - input dataset:
      - Player Training.csv
  - output dataset (for results check only):
      - 2022W42.csv
"""


from numpy import where
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\Player Training.csv', parse_dates=['Date'], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create all combinations of Player, Session, and Date
df_dates = pd.DataFrame({'Date' : pd.date_range(start=df['Date'].min(), 
                                                end=df['Date'].max(), 
                                                freq='1D')})

df_all = ( df[['Player', 'Session']].drop_duplicates()
               .merge(df_dates, how='cross')
               .merge(df, on=['Player', 'Session', 'Date'], how='left')
               .sort_values(by=['Player', 'Session', 'Date']) )
             
             
# flag actual vs. carried over from previous session
df_all['Flag'] = where(df_all['Score'].isna(), 'Carried over', 'Actual')


# fill down the scores
df_all['Score'] = df_all.groupby(['Player', 'Session'])['Score'].ffill()


# remove missing scores (dates before the player's first session) and weekends
df_all = ( df_all.loc[(df_all['Score'].notna()) & (df_all['Date'].dt.weekday <= 4)]
                 .rename(columns={'Date' : 'Session Date'}) )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_all.to_csv(r'.\outputs\output-2022-42.csv', index=False, float_format='%f', date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W42.csv']
my_files = [r'.\outputs\output-2022-42.csv']
unique_cols = [['Player', 'Session', 'Session Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)




#---------------------------------------------------------------------------------------------------
# testing different options for getting the next date
#---------------------------------------------------------------------------------------------------

# option 1 - create all player/session/date combos and merge/filldown -- FASTEST

# original dataset = 26.3 ms ± 2.47 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 1.1M records     = 4.44 s ± 127 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
# create all combinations of Player, Session, and Date
df_dates = pd.DataFrame({'Date' : pd.date_range(start=df['Date'].min(), 
                                                end=df['Date'].max(), 
                                                freq='1D')})
df_all = df[['Player', 'Session']].drop_duplicates()\
             .merge(df_dates, how='cross')\
             .merge(df, on=['Player', 'Session', 'Date'], how='left')\
             .sort_values(by=['Player', 'Session', 'Date'])
             
# flag actual vs. carried over from previous session
df_all['Flag'] = where(df_all['Score'].isna(), 'Carried over', 'Actual')

# fill down the scores
df_all['Score'] = df_all.groupby(['Player', 'Session'])['Score'].ffill()

# remove missing scores (dates before the player's first session) and weekends
df_all = df_all.loc[(df_all['Score'].notna()) & (df_all['Date'].dt.weekday <= 4)]\
             .rename(columns={'Date' : 'Session Date'})




# option 2a - merge_asof, create date ranges, explode -- SLOW

# 863 ms ± 47.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
# find the next available date by player/session
df = df.sort_values(by='Date')
df_all = pd.merge_asof(df, 
                       df[['Player', 'Session', 'Date']].rename(columns={'Date' : 'Next Date'}), 
                       left_on='Date', right_on='Next Date', by=['Player', 'Session'], 
                       direction='forward', allow_exact_matches=False)

# fill missing dates with the max date + 1
df_all['Next Date'] = df_all['Next Date'].fillna(df_all['Date'].max() + pd.Timedelta(days=1))

# list of dates to add
df_all['Session Date'] = [pd.date_range(start=s, end=e - pd.Timedelta(days=1), freq='1D') 
                          for s, e in zip(df_all['Date'], df_all['Next Date'])]
df_all = df_all.explode('Session Date')

# flag actual vs. carried over from previous session
df_all['Flag'] = where(df_all['Session Date'] != df_all['Date'], 'Carried over', 'Actual')

# remove missing scores (dates before the player's first session) and weekends
df_all = ( df_all.loc[(df_all['Score'].notna()) & (df_all['Session Date'].dt.weekday <= 4)]
                 .drop(columns=['Date', 'Next Date']) )




# option 2b - shift to get next date -- SLOWEST

# 966 ms ± 146 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
# find the next available date by player/session
df = df.sort_values(by=['Player', 'Session', 'Date'])
df['Next Date'] = df.groupby(['Player', 'Session'])['Date'].shift(-1)


# fill missing dates with the max date + 1
df['Next Date'] = df['Next Date'].fillna(df['Date'].max() + pd.Timedelta(days=1))

# list of dates to add
df['Session Date'] = [pd.date_range(start=s, end=e - pd.Timedelta(days=1), freq='1D') 
                          for s, e in zip(df['Date'], df['Next Date'])]
df_all = df.explode('Session Date')

# flag actual vs. carried over from previous session
df_all['Flag'] = where(df_all['Session Date'] != df_all['Date'], 'Carried over', 'Actual')

# remove missing scores (dates before the player's first session) and weekends
df_all = ( df_all.loc[(df_all['Score'].notna()) & (df_all['Session Date'].dt.weekday <= 4)]
                 .drop(columns=['Date', 'Next Date']) )




# option 3 - merge ordered -- SLOW

# 93.3 ms ± 8.09 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

%%timeit 
df_dates = pd.DataFrame({'Session Date' : pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='1D')})

df_all = pd.merge_ordered(df, df_dates,
                          left_by=['Player', 'Session'], left_on='Date', right_on='Session Date',
                          fill_method='ffill')

df_all['Flag'] = where(df_all['Date'] == df_all['Date'].shift(1), 'Carried over', 'Actual')

# remove weekends
df_all = ( df_all[df_all['Session Date'].dt.weekday <= 4]
                 .drop(columns=['Date']) )




# option 4 - indexing -- similar performance to option 1, but option 1 is faster on a larger dataset

# original dataset = 28 ms ± 2.06 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 1.1M records     = 5.22 s ± 130 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
# pad out the missing dates by creating a multiindex of all possible combinations
all_dates = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='1D')

new_idx = pd.MultiIndex.from_product([df['Player'].unique(), 
                                      df['Session'].unique(), 
                                      all_dates], 
                                     names=['Player', 'Session', 'Date'])

df_all = ( df.set_index(['Player', 'Session', 'Date'])
             .reindex(new_idx)
             .reset_index() )


# add carried over vs. actual flag
df_all['Flag'] = where(df_all['Score'].isna(), 'Carried over', 'Actual')

# fill down the score
df_all['Score'] = df_all.groupby(['Player', 'Session'])['Score'].ffill()

# remove weekends and dates prior to the first session date
df_all = ( df_all[(df_all['Date'].dt.weekday <= 4) & (df_all['Score'].notna())]
                 .rename(columns={ 'Date' : 'Session Date'}) )
