# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 17 - The Price of Streaming
https://preppindata.blogspot.com/2022/04/2022-week-17-price-of-streaming.html

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
Created: 2022-05-10
Requirements:
  - input dataset:
      - 2022W17 Input.xlsx
  - output dataset (for results check only):
      - 2022W17 Output.csv
  - output_check module (for results check only)

"""


from numpy import where
import pandas as pd
import output_check  # custom module for comparing output to the solution file


LOCATION_RENAMES = {'Edinurgh' : 'Edinburgh'}
CONTENT_TYPES = {'Primary' : ['Cardiff', 'Edinburgh', 'London']}


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\2022W17 Input.xlsx') as xl:
    
    # input the streaming data, fix location spelling, sum the duration by session
    df_s = pd.read_excel(xl, sheet_name='Streaming', parse_dates=['t'])\
             .assign(location=lambda df_x: df_x['location'].replace(LOCATION_RENAMES))\
             .rename(columns={'t' : 'timestamp'})\
             .groupby(['userID', 'timestamp', 'location', 'content_type'], 
                      as_index=False, dropna=False)['duration'].sum()
    
    # input the pricing data
    df_p = pd.read_excel(xl, 'Avg Pricing', parse_dates=['Month'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# adjust the content type
df_s['content_type'] = where(df_s['location'].isin(CONTENT_TYPES['Primary']), 'Primary',
                          where(df_s['content_type'] == 'Preserved', df_s['content_type'], 
                                'Secondary'))

# add the pricing month
# for Primary content --> overall minimum month
# for all other cotent --> minimum month by user/location/content type
df_s['Month'] = where(df_s['content_type']=='Primary', 
                      df_s.groupby(['userID'])['timestamp']\
                          .transform('min').dt.tz_localize(None).astype('datetime64[M]'), 
                      df_s.groupby(['userID', 'location', 'content_type'])['timestamp']\
                          .transform('min').dt.tz_localize(None).astype('datetime64[M]'))

    
# join to pricing table and fill in avg price for preserved content
df_out = df_s.merge(df_p.rename(columns={'Content_Type' : 'content_type'}), 
                    on=['Month', 'content_type'], how='left')\
             .drop(columns='Month')\
             .assign(Avg_Price=lambda df_x: where(df_x['content_type']=='Preserved', 14.98,
                                                  df_x['Avg_Price']))


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-17.csv', index=False, date_format='%d/%m/%Y %H:%M:%S')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W17 Output.csv']
my_files = [r'.\outputs\output-2022-17.csv']
unique_cols = [['userID', 'timestamp', 'location', 'content_type']]
col_order_matters = True
round_dec = 8

output_check.output_check(solution_files, my_files, unique_cols, col_order_matters = False)


#---------------------------------------------------------------------------------------------------
# experimenting with different methods for truncating the timestamp to the first of the month
#---------------------------------------------------------------------------------------------------

# converting to string and back to date (expect this to be inefficient, but not sure how much)
# slowest: 4.27 ms ± 236 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
%%timeit 
df_s['month_1'] = pd.to_datetime(df_s['timestamp'].dt.strftime('%Y-%m-01'))


# dateoffset
# much better: 920 µs ± 198 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
%%timeit 
df_s['month_2'] = df_s['timestamp'] + pd.offsets.Day() - pd.offsets.MonthBegin()


# changing the type
# fastest: 719 µs ± 52.1 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
%%timeit 
df_s['month_3'] = df_s['timestamp'].dt.tz_localize(None).astype('datetime64[M]')

