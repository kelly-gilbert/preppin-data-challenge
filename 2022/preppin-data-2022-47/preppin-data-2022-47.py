# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 47 - Chelsea Managers per Prime Minister
https://preppindata.blogspot.com/2022/11/2022-week-47-chelsea-managers-per-prime.html

- Input the data
- For the Prime Ministers data:
  - Group together Sir Winston Churchill and Winston Churchill
  - Split the dates to create Start Date PM and End Date PM
    - For the null End Date PM, replace with today's date
  - Create a row for every day the Prime Minister was in office
- For the Chelsea Manager data:
  - Remove unnecessary fields and rename remaining fields
  - Clean the Chelsea Managers field
  - For the null End Date CM, replace with today's date
  - Create a row for every day the Chelsea Manager was in place
- For the Chelsea Matches data:
  - Filter to only include the main competitive matches:
    - League
    - League Cup
    - F.A. Cup
    - Europe
  - Make sure the Date is a Date Data Type
  - Pivot the data so we know how many matches were won, drawn or lost on each day
  - Create a Matches field, so we know the number of matches played each day
- Bring the 3 datasets together
- Aggregate so that we are able to count the number of Chelsea Managers for each Prime Minister, as well as how many Matches were played during their time in office and the breakdown of their outcome
- Calculate the Win % for each Prime Minister
  - i.e. Matches Won / Total Matches
  - Rounded to 2 d.p.
- Output the data

Author: Kelly Gilbert
Created: 2023-02-27
Requirements:
  - input dataset:
      - Chelsea Managers.xlsx
      - Chelsea Matches.csv
      - Prime Ministers.xlsx
  - output dataset (for results check only):
      - Chelsea Managers per Prime Minister.csv
"""


from datetime import date
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in the prime ministers, correct name, split dates
df_pm = ( pd.read_excel(r'.\inputs\Prime Ministers.xlsx')
            .replace('Winston Churchill', 'Sir Winston Churchill') )

df_pm[['Start Date PM', 'End Date PM']] = ( df_pm['Duration']
                                                 .str.extract('(.*?)-\s(.*)')
                                                 .replace({'Present' : date.today()})
                                                 .apply(lambda x: pd.to_datetime(x)) )


# read in the Chelsea managers, clean names, replace present with today's date
df_mgr = ( pd.read_excel(r'.\inputs\Chelsea Managers.xlsx', 
                         usecols=['Name', 'From', 'To'],
                         parse_dates=['From', 'To'])
             .assign(Name = lambda df_x: df_x['Name'].str.replace('\[.*', '', regex=False),
                     To = lambda df_x: pd.to_datetime(df_x['To'].replace('Present', date.today()))) )


# read in the match data, limited to specific competition types
df_matches = ( pd.read_csv(r'.\inputs\Chelsea Matches.csv', 
                           encoding='latin_1',
                           usecols=['Comp', 'Date', 'Result'],
                           parse_dates=['Date'])
                 .query("Comp == ['League', 'League Cup', 'F.A. Cup', 'Europe']") )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# Chelsea managers per PM
df_pm_mgr = ( df_pm.merge(df_mgr, how='cross')
                   .query("To >= `Start Date PM` & From <= `End Date PM`")
                   .groupby(['Prime Ministers', 'Duration'], as_index=False)
                   .agg(Chelsea_Managers=('Name', 'count')) )


# count of matches per PM                
df_pm_matches = ( df_pm.merge(df_matches, how='cross')
                       .query("Date >= `Start Date PM` & Date <= `End Date PM`")
                       .pivot_table(index=['Prime Ministers', 'Duration'],
                                    columns='Result',
                                    values='Comp',
                                    aggfunc='count',
                                    margins=True, margins_name='Matches')
                       .rename(columns=lambda c: c.replace('Match ', 'Matches '))
                       .reset_index() )


# assemble final table
df_out = ( df_pm.merge(df_pm_mgr, how='left', on=['Prime Ministers', 'Duration'])
                .merge(df_pm_matches, how='left', on=['Prime Ministers', 'Duration'])
                .rename(columns=lambda c: c.replace('_', ' '))
                .drop(columns='Duration')
                .fillna(0) ) 
df_out['Win %'] =round(df_out['Matches Won'] / df_out['Matches'], 2)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-47.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Chelsea Managers per Prime Minister.csv']
my_files = [r'.\outputs\output-2022-47.csv']
unique_cols = [['Prime Ministers', 'Start Date PM']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
