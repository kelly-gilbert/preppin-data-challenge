# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 26 - Making Spotify Data Spotless
https://preppindata.blogspot.com/2022/06/2022-week-26-making-spotify-data.html

- Input the data
- Create a new field which would break down milliseconds into seconds and minutes
  e.g. 208,168 turned into minutes would be 3.47min
- Extract the year from the timestamp field
- Rank the artists by total minutes played overall
- For each year, find the ranking of the artists by total minutes played
- Reshape the data so we can compare how artist position changes year to year
- Filter to the overall top 100 artists
- Output the data

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input dataset:
      - Spotify Data Unclean.csv
  - output dataset (for results check only):
      - 2022W26 Output.csv
"""


from numpy import floor
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution





def round_half_up(n, decimals=0):
    """ 
    use round half up method vs. Python default rounding
    """
    multiplier = 10 ** decimals
    # Replace math.floor with np.floor
    return floor(n*multiplier + 0.5) / multiplier



#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\Spotify Data Unclean.csv', parse_dates=['ts'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# convert milliseconds to minutes and extract the year
df['min'] = round_half_up(df['ms_played'] / 1000 / 60 * 100, 0)
df['year'] = df['ts'].dt.year


# option 2: pivot the minutes, then rank
df_out = ( pd.pivot_table(df,
                          index='Artist Name',
                          columns='year',
                          values='min',
                          aggfunc='sum',
                          margins=True, margins_name='Overall Rank')
             .query("index != 'Overall Rank'")
             .apply(lambda x: x.rank(ascending=False, method='min', axis=0)) 
             .reset_index()
             .query("`Overall Rank` <= 100") )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-26.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W26 Output.csv']
my_files = [r'.\outputs\output-2022-26.csv']
unique_cols = [['Artist Name']]
col_order_matters = False
round_dec = 8

output_check(solution_files, my_files, unique_cols, col_order_matters = False)







df_sum[(df_sum['Artist Name']=='Nobuo Uematsu')]

df[(df['Artist Name']=='Nobuo Uematsu') & (df['year']==2015)]['min'].sum()

df[(df['Artist Name']=='Robert Schumann') & (df['year']==2015)]['min'].sum()


df_sol[df_sol['Artist Name'].eq('Rise Against')]
df_sol[df_sol['Artist Name'].eq('Rise Against')]


df_sol.sort_values('2015').iloc[40:60]
df_out.sort_values('2015').iloc[120:140]

df_out[df_out['Overall Rank'].gt(85) & df_out['Overall Rank'].lt(100)].sort_values('Overall Rank')

df_sol = pd.read_csv(solution_files[0])


df[df['Artist Name'].isin(['Rise Against', 'Nobuo Uematsu', 'Puddle of Mudd'])].groupby('Artist Name')['min'].sum()
