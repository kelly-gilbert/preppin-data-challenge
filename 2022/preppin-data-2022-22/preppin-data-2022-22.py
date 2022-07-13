# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 22 - Dungeons & Dragons: Critical Role
https://preppindata.blogspot.com/2022/06/2022-week-22-dungeons-dragons-critical.html

- Input the data
- To create our gantt chart we'll need to work out how long each character is talking. To do this 
  we can work out the difference from one timestamp to the next. However for the last lines of 
  dialogue we'll need to know when the episode ends. To do this we'll need to union the dialogue with the episode details to find the last timestamp
- Create a rank of the timestamp for each episode, ordered by earliest timestamp
  - Think carefully about the type of rank you want to use
- Create a new column that is -1 the rank, so we can lookup the next line
- Create a duplicate dataset and remove all columns except
  - episode
  - next_line
  - time_in_secs
- Inner join these two datasets
- Calculate the dialogue durations
- Some character names are comma separated, split these names out and trim any trailing whitespace
  - It's ok to leave "ALL" as "ALL"
- Reshape the data so we have a row per character
- Filter the data for just Gameplay sections
- Ensure no duplication of rows has occurred
- Output the data

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input dataset:
      - Critical_Role_Campaign_1_Datapack.xlsx
  - output dataset (for results check only):
      - 2022W22 Output.csv
"""


from numpy import where
import pandas as pd
from output_check import output_check


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\Critical_Role_Campaign_1_Datapack.xlsx') as xl:
    df_eps = pd.read_excel(xl, sheet_name='episode_details')
    df_dialogue = pd.read_excel(xl, sheet_name='dialogue')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# get the next timestamp and filter to Gameplay sections
df_out = ( pd.merge_asof(df_dialogue.sort_values(by=['time_in_secs'])
                             .rename(columns={'time_in_secs' : 'start_time'}), 
                         df_dialogue[['Episode', 'time_in_secs']].sort_values(by=['time_in_secs'])
                             .rename(columns={'time_in_secs' : 'end_time'}), 
                         left_on='start_time', right_on='end_time', by=['Episode'], 
                         direction='forward', allow_exact_matches=False)
             .query("section == 'Gameplay'")
         )


# set the end time and calculate the duration
df_out['Duration'] = ( where(df_out['end_time'].isna(), 
                             df_out['Episode'].replace(dict(zip(df_eps['Episode'], 
                                                                 df_eps['runtime_in_secs']))), 
                             df_out['end_time'])
                       - df_out['start_time']
                     ).astype(int)


# split (duplicate) if there are multiple characters in name
df_out = ( df_out.assign(name=df_out['name'].str.replace(' ', '').str.split(','),
                         dialogue=df_out['dialogue'].astype(str).str.strip())
                 .explode('name')
                 .drop(columns=['end_time'])
                 .drop_duplicates()
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-22.csv', index=False, 
              columns=['Episode', 'name', 'start_time', 'Duration', 'youtube_timestamp', 
                       'dialogue', 'section'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W22 Output.csv']
my_files = [r'.\outputs\output-2022-22.csv']
unique_cols = [['Episode', 'name', 'start_time', 'dialogue']]
col_order_matters = True
round_dec = 6

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)


#---------------------------------------------------------------------------------------------------
# options for getting the next timestamp
#---------------------------------------------------------------------------------------------------

# option 1: rank lines within episode, merge to get next line
# 7.46 s ± 213 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) -- SLOW

%%timeit 
df_dialogue['rank_in_ep'] = df_dialogue.groupby(['Episode'])['time_in_secs'].rank()
df_dialogue['next_rank'] = df_dialogue['rank_in_ep'] + 1
df_out = df_dialogue.merge(df_dialogue[['Episode', 'next_rank', 'time_in_secs']], how='left', 
                           left_on='rank_in_ep', right_on='next_rank')


# option 2: merge_asof forward
# 377 ms ± 21.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) -- MUCH FASTER

%%timeit 
df_out = ( pd.merge_asof(df_dialogue.sort_values(by=['time_in_secs']), 
                         df_dialogue[['Episode', 'time_in_secs']].sort_values(by=['time_in_secs'])
                             .rename(columns={'time_in_secs' : 'end_time_in_secs'}), 
                         left_on=['time_in_secs'], right_on='end_time_in_secs', by=['Episode'], 
                         direction='forward', allow_exact_matches=False)
         )


# option 3: use index
# 241 ms ± 10.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) -- FASTEST!
# however, this doesn't work correctly, because there are duplicate timestamps when the actors
#    talk over each other

%%timeit 
df_out = pd.merge_asof(df_dialogue, df_dialogue[['Episode', 'time_in_secs']], 
                       by='Episode', left_index=True, right_index=True, direction='forward',
                       allow_exact_matches=False)
