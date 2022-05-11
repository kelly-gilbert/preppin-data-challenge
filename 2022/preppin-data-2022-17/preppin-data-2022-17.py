# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 17 - challenge title goes here
https://preppindata.blogspot.com/ - challenge url goes here

- Input data
- Check the location field for spelling errors
    - Data roles may help you identify these
- Fix the date fields so they are recognised as date data types
- Aggregate the data to find the total duration of each streaming session (as identified by the timestamp)
- We need to update the content_type field:
    - For London, Cardiff and Edinburgh, the content_type is defined as "Primary"
    - For other locations, maintain the "Preserved" content_type and update all others to have a 
      "Secondary" content_type
- To join to the Avg Pricing Table, we need to work out when each user's first streaming session was.
  However, it's a little more complex than that. 
    - For "Primary" content, we take the overall minimum streaming month, ignoring location
    - For all other content, we work out the minimum active month for each user, in each location and 
      for each content_type
- We're now ready to join to the Avg Pricing Table
- For "Preserved" content, we manually input the Avg Price as £14.98
- Output the data

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input dataset:
      - 2022W17 Input.xlsx
  - output dataset (for results check only):
      - 2022W17 Output.csv
  - output_check module (for results check only)

"""


from numpy import where
import pandas as pd


LOCATION_RENAMES = {'Edinurgh' : 'Edinburgh'}
CONTENT_TYPES = {'Primary' : ['Cardiff', 'Edinburgh', 'London'],
                 'Secondary' : ['Bristol', 'Cornwall', 'Kent', 'Newcastle', 'Norfolk', 'Plymouth']}


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\2022W17 Input.xlsx') as xl:
    
    # input the streaming data and sum the duration
    df_s = pd.read_excel(xl, sheet_name='Streaming', parse_dates=['t'])\
             .assign(location=lambda df_x: df_x['location'].replace(LOCATION_RENAMES))\
             .rename(columns={'t' : 'timestamp'})\
             .groupby(['userID', 'timestamp', 'location'], as_index=False)['duration'].sum()
    
    df_p = pd.read_excel(xl, 'Avg Pricing', parse_dates=['Month'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# add the content type
df_s['content_type'] = where(df_s['location'].isin(CONTENT_TYPES['Primary']), 'Primary',
                          where(df_s['location'].isin(CONTENT_TYPES['Secondary']), 'Secondary',
                                'Preserved'))

# add the pricing month
# for Primary content --> overall minimum month
# otherwise, minimum month by user/location/content type
df_s['Month'] = where(df_s['content_type']=='Primary', 
                      df_s.groupby(['userID'])['timestamp'].transform('min').dt.normalize(), 
                      df_s.groupby(['userID', 'location', 'content_type'])['timestamp'].transform('min').dt.normalize())\
    .astype('datetime64[M]')



df_s[['userID', 'content_type', 'Month']].iloc[0:50]

df_out = df_s.merge(df_p.rename(columns={'Content_Type' : 'content_type'}), 
                    on=['Month', 'content_type'], how='left')

- For "Preserved" content, we manually input the Avg Price as £14.98



#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-17.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['2022W17 Output.csv']
my_files = ['output-2022-17.csv']
unique_cols = ['Month']
col_order_matters = True
round_dec = 8

output_check.output_check(solution_files, my_files, unique_cols, col_order_matters = False)
