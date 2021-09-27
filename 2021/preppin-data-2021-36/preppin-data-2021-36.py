# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 36 - What's Trendy?
https://preppindata.blogspot.com/2021/09/2021-week-36-whats-trendy.html

- Input the data
- Calculate the overall average index for each search term
- Work out the earliest peak for each of these search terms
- For each year (1st September - 31st August), calculate the average index
- Classify each search term as either a Lockdown Fad or Still Trendy based on whether the average
  index has increased or decreased since last year
- Filter the countries so that only those with values for each search term remain
- For each search term, work out which country has the highest percentage
- Bring everything together into one dataset
- Output the data

Author: Kelly Gilbert
Created: 2021-09-08
Requirements:
  - input dataset:
      - Trend Input.xlsx
  - output dataset (for results check only):
      (no output dataset this week)
"""

from numpy import nan, where
from pandas import ExcelFile, melt, merge, read_excel


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Trend Input.xlsx') as xl:
    df_t = read_excel(xl, sheet_name='Timeline', skiprows=2)\
           .melt(id_vars='Week', var_name='Search Term', value_name='index')
    df_c = read_excel(xl, sheet_name='Country Breakdown', skiprows=2)\
           .melt(id_vars='Country', var_name='Search Term', value_name='pct')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# clean the search term name
df_t['Search Term'] = df_t['Search Term'].str.replace(':.*', '')
df_c['Search Term'] = df_c['Search Term'].str.replace(':.*', '')


# find the year for each week
df_t['year'] = df_t['Week'].dt.year + where(df_t['Week'].dt.month >= 9, 1, 0)


# find the overall and CY avg, calculate status, get earliest peak
max_year = df_t['year'].max()
df_t['CY_index'] = where(df_t['year']==max_year, df_t['index'], nan)
df_t['LY_index'] = where(df_t['year']==max_year-1, df_t['index'], nan)
df = df_t.groupby('Search Term').agg(Avg_index = ('index', 'mean'),
                                     CY_index = ('CY_index', 'mean'),
                                     LY_index = ('LY_index', 'mean'),
                                     idxmax = ('index', 'idxmax')).reset_index()

df['Status'] = where(df['CY_index'] >= df['LY_index'], 'Still trendy', 'Lockdown Fad')

df[['CY_index', 'Avg_index']] = df[['CY_index', 'Avg_index']].round(1)

df['Index Peak'] = df_t.iloc[df['idxmax']]['index'].reset_index(drop=True)
df['First Peak'] = df_t.iloc[df['idxmax']]['Week'].reset_index(drop=True)


# filter out countries that are missing one or more terms,
# get country with the % for each term
df_c = df_c.loc[~df_c['Country'].isin(df_c[df_c['pct'].isna()]['Country'].unique())]\
           .sort_values('pct', ascending=False)\
           .groupby('Search Term').first()\
           .reset_index()

df = df.merge(df_c, on='Search Term')


# rename columns
df.rename(columns={ 'CY_index' : f'{max_year-1}/{str(max_year)[-2:]} avg index', 
                    'Avg_index':'Avg index',
                    'Country' : 'Country with highest percentage'}, inplace=True)
                   
                                
#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

cols = ['Search Term', 'Status', '2020/21 avg index', 'Avg index', 'Index Peak', 'First Peak', 
        'Country with highest percentage']
df.to_csv(r'.\outputs\output-2021-36.csv', index=False, columns=cols, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# solution checked by visual inspection this week
