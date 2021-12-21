# -*- coding: utf-8 -*-
"""
Preppin' Data 2020: Week 04 - challenge title goes here
https://preppindata.blogspot.com/ - challeng url goes here

- Input data
- Change the Question Number for the question asked


- Clean the Country and Store names
  - We only want English names for places
- Clean up the dates and times to create a 'Completion Date' as a Date Time field
- Understand the age of the customer based on their Date of Birth (DoB)
  - Nulls are ok
  - Their age is taken to the date of 22nd January 2020
- Find the first answer for each customer in each store and country
- Find the latest answer for each customer in each store and country (if there
  are multiple responses)
- Remove any answers that are not a customer's first or latest
- Classify the 'NPS Recommendation' question based on the standard logic:
  - 0-6 makes the customer a 'Detractor'
  - 7-8 makes the customer a 'Passive' 
  - 9-10 makes the customer a 'Promoter'
- Output the data

Author: Kelly Gilbert
Created: 2020-MM-DD
Requirements:
  - input datasets:
      - PD 2020 Wk 4 Input.csv
      - Store Survey Results - Question Sheet.csv
  - output dataset (for results check only):
      - PD 2020 Wk 4 Output
"""


import datetime as dt
from dateutil.relativedelta import relativedelta
from numpy import ceil, NaN, timedelta64, where
from pandas import pivot_table, read_csv, to_datetime


def split_dict(in_dict):
    """
    add the list of misspelled names as keys, with the correct spelling as the value
    """
    
    new_dict = { i:k for k, v in in_dict.items() for i in v}    
    new_dict.update({ k.lower() : k.title() for k in in_dict.keys() })
    return new_dict


CURRENT_DATE = dt.datetime(2020, 1, 22)


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\inputs\PD 2020 Wk 4 Input.csv', parse_dates=['DoB'], dayfirst=True)
df_q = read_csv(r'.\inputs\Store Survey Results - Question Sheet.csv')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# clean the Country and Store names
#df['Country'].unique()
#df['Store'].unique()

country_dict = { 'England' : ['3ngland', 'egland', 'eggland', 'ingland'],
                 'Scotland' : ['sc0tland', 'scottish'],
                 'United States' : ['united state'],
                 'Netherlands' : ['the netherlands'] }

store_dict = { 'Amsterdam' : ['amstelveen']}

df['Country'] = df['Country'].str.lower().replace(split_dict(country_dict)).str.title()
df['Store'] = df['Store'].str.lower().replace(split_dict(store_dict)).str.title()


# pivot questions into columns
df_p = df.pivot_table(values='Answer', columns='Question Number', 
                      index=[c for c in df.columns if c not in['Answer', 'Question Number']],
                      aggfunc='first').reset_index()

question_dict = {n : q for n, q in zip(df_q['Number'], df_q['Question'])}
df_p.columns = [question_dict.get(c, c) for c in df_p.columns]


# clean date and time
df_p['Date'] = to_datetime(df_p['What day did you fill the survey in?'],
                           dayfirst=True, errors='coerce')
max_yr = int(df_p['Date'].dt.year.max())
df_p['Date'] = where(df_p['Date'].isna(), 
                     to_datetime(df_p['What day did you fill the survey in?']
                               .str.replace('.* - (.*)', '\\1 ' + str(max_yr), regex=True)),
                     df_p['Date'])


df_p['Time'] =to_datetime(df_p['What time did you fill the survey in?']\
                              .str.replace('.', ':', regex=False)\
                              .str.replace('24(\:?\d{2})', '00\\1', regex=True)\
                              .str.replace('(\d{2})(\d{2})', '\\1:\\2', regex=True))
    
df_p['Completion Date'] = to_datetime(df_p['Date'].astype(str) + ' ' + df_p['Time'].dt.strftime('%H:%M:%S'))


# understand the age of the customer based on their Date of Birth (DoB)
df_p['Age of Customer'] = [relativedelta(CURRENT_DATE, d).years for d in df_p['DoB']]


# remove any answers that are not a customer's first or latest
group_cols = ['Name', 'Store', 'Country']
df_p['Result'] = where(df_p['Completion Date'] == df_p.groupby(group_cols)['Completion Date'].transform('min'),
                       'First',
                       where(df_p['Completion Date'] == df_p.groupby(group_cols)['Completion Date'].transform('max'),
                             'Latest', NaN))
df_p = df_p.loc[df_p['Result'].notna()]


# classify NPS recommendation
score_field = 'Would you recommend C&BSco to your friends and family? (Score 0-10)'
df_p['Detractor'] = where(df_p[score_field].astype(int) <= 6, 1, NaN)
df_p['Passive'] = where((df_p[score_field].astype(int) >= 7) 
                        & (df_p[score_field].astype(int) <= 8), 1, NaN)
df_p['Promoter'] = where(df_p[score_field].astype(int) > 8, 1, NaN)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

cols = ['Country', 'Store', 'Name', 'Completion Date', 'Result',
       'Would you recommend C&BSco to your friends and family? (Score 0-10)',
       'Promoter', 'Detractor', 'Passive', 'Age of Customer',
       'If you wouldn\'t, why?', 'If you would, why?']
df_p.to_csv(r'.\outputs\output-2020-04.csv', columns=cols, index=False, date_format='%d/%m/%Y %H:%M:%S')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2020 Wk 4 Output.csv']
my_files = ['output-2020-04.csv']
col_order_matters = True

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_file)
    df_mine = read_csv('.\\outputs\\' + my_files[i])
    
    df_solution.drop(columns='Age of Customer', inplace=True)
    df_mine.drop(columns='Age of Customer', inplace=True)

    # are the fields the same and in the same order?
    solution_cols = list(df_solution.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_solution.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        # round float values
        s = df_solution.dtypes.astype(str)
        for c in s[s.str.contains('float')].index:
            df_solution[c] = df_solution[c].round(8)
            df_mine[c] = df_mine[c].round(8)

        # join the dataframes on all columns except the in flags
        df_solution_compare = df_solution.merge(df_mine, how='outer',
                                                on=list(df_solution.columns),
                                                suffixes=['_solution', '_mine'], indicator=True)

        if len(df_solution_compare[df_solution_compare['_merge'] != 'both']) > 0:
            print('*** Values do not match ***\n')
            print('In solution, not in mine:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'left_only']) 
            print('\n\n')
            print('In mine, not in solution:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'right_only']) 
            
        else:
            print('Values match')

    print('\n')


df_solution_compare.iloc[9]
country = 'England'
store = 'Clapham'
Name = 'Juliana'
date = '05/01/2020 13:03:00'
df_solution[df_solution['Completion Date']==date].iloc[0]
df_mine[df_mine['Completion Date']==date].iloc[0]


df_mine[df_mine['Name']=='James Cagney'].iloc[0]

x = df_p[df_p['Name']=='Gwilym']
(CURRENT_DATE - x['DoB']) / timedelta64(1, 'Y')
df_mine[df_mine['Completion Date']=='20/05/2019 23:00:00']

df_p[df_p['Name']=='James Cagney'].iloc[0]

df['Name'].unique()
