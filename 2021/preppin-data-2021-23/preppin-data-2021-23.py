# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 23 - NPS for Airlines
https://preppindata.blogspot.com/2021/06/2021-week-23-nps-for-airlines.html

- Input the data
- Combine Prep Air dataset with other airlines
- Exclude any airlines who have had less than 50 customers respond
- Classify customer responses to the question in the following way:
    - 0-6 = Detractors
    - 7-8 = Passive
    - 9-10 = Promoters
- Calculate the NPS for each airline
  NPS = % Promoters - % Detractors
  Note: I rounded the %s down to the nearest whole number, so if your answer differs slightly from
  mine then this could be why! 
- Calculate the average and standard deviation of the dataset
- Take each airline's NPS and subtract the average, then divide this by the standard deviation
- Filter to just show Prep Air's NPS along with their Z-Score
- Output the data

Author: Kelly Gilbert
Created: 2021-06-09
Requirements:
  - input dataset:
      - NPS Input.xlsx
"""

from numpy import floor
from pandas import concat, cut, DataFrame, ExcelFile, read_excel

# for results check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\NPS Input.xlsx') as xl:
    df = concat([read_excel(xl, s) for s in xl.sheet_names])   
        

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# response count by airline
df = df.groupby('Airline').filter(lambda x: len(x) >= 50) 

# classify customer responses to the question in the following way
#     0-6 = Detractors, 7-8 = Passive, 9-10 = Promoters
df['nps_type'] = cut(df['How likely are you to recommend this airline?'], bins=[0, 6, 8, 10],
                     labels=['Detractors', 'Passive', 'Promoters'], right=True, 
                     include_lowest=True).astype(str)
    
# calculate the NPS for each airline (rounded down to nearest %)
df_pivot = df.pivot_table(values=['CustomerID'], index=['Airline'], columns=['nps_type'], 
                          aggfunc='count', fill_value=0).reset_index()
df_pivot.columns = [c[1] if c[1] != '' else c[0] for c in df_pivot.columns]

df_pivot['total'] = df_pivot['Detractors'] + df_pivot['Passive'] + df_pivot['Promoters']

df_pivot['NPS'] = (floor(df_pivot['Promoters'] / df_pivot['total'] * 100) \
                   - floor(df_pivot['Detractors'] / df_pivot['total'] * 100)).astype(int)

# calculate the average and standard deviation of the dataset
nps_mean = df_pivot['NPS'].mean()
nps_std = df_pivot['NPS'].std()

# take each airline's NPS and subtract the average, then divide this by the standard deviation
df_pivot['Z-Score'] = (df_pivot['NPS'] - nps_mean) / nps_std


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Airline', 'NPS', 'Z-Score']
df_pivot[df_pivot['Airline']=='Prep Air'].to_csv(r'.\outputs\output-2021-23.csv', index=False, 
                                                 columns=out_cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

my_results = read_csv(r'.\outputs\output-2021-23.csv')
my_results
