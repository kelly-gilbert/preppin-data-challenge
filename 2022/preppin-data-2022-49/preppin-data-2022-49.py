# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 49 - Cleaning Status History (HR month)
https://preppindata.blogspot.com/2022/12/2022-week-49-cleaning-status-history-hr.html

- Input the data
- For each combination of candidate and position, find the most recent file. 
  - Watch out - the vendor has not been consistent with file naming. However, the file timestamp is 
    always the 19 characters before “.csv”
  - Filter out any records that are not from the most recent file
- Output the data

Author: Kelly Gilbert
Created: 2022-12-19
Requirements:
  - input dataset:
      - status_history_raw.csv
  - output dataset (for results check only):
      - status_history_clean.csv
      - current_status.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\status_history_raw.csv', parse_dates=['ts'], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# find the latest filename per candidate/position, then return only the statuses for those files
df['file_date'] = df['filename'].str[-23:-4]

df_keep = ( df.merge(df.groupby(['candidate_id', 'position_id'])['file_date'].max(),
                     on=['candidate_id', 'position_id', 'file_date'])
              .drop(columns='file_date') )


# find the current status for each person
df_current = ( df_keep.loc[df_keep.groupby(['candidate_id', 'position_id'])['ts'].idxmax()]
                      .drop(columns=['filename', 'ts'])
                      .rename(columns={'status' : 'current_status'}) )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_keep.to_csv(r'.\outputs\output-2022-49-status_history_clean.csv', index=False, date_format='%d/%m/%Y %H:%M:%S')

df_current.to_csv(r'.\outputs\output-2022-49-current_status.csv', index=False)


# what is the current status of candidate 114, position 9?
print(df_current.query('candidate_id == 114 & position_id == 9'))


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\status_history_clean.csv', r'.\outputs\current_status.csv']
my_files = [r'.\outputs\output-2022-49-status_history_clean.csv', r'.\outputs\output-2022-49-current_status.csv']
unique_cols = [['candidate_id', 'position_id', 'status', 'ts', 'filename'],
               ['candidate_id', 'position_id']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
