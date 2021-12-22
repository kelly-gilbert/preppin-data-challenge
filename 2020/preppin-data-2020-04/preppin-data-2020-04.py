# -*- coding: utf-8 -*-
"""
Preppin' Data 2020: Week 04
https://preppindata.blogspot.com/2020/01/2020-week-4.html

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
Created: 2021-12-20
Requirements:
  - input datasets:
      - PD 2020 Wk 4 Input.csv
      - Store Survey Results - Question Sheet.csv
  - output dataset (for results check only):
      - PD 2020 Wk 4 Output
"""


import datetime as dt
from numpy import nan, where
from pandas import pivot_table, read_csv, to_timedelta, to_datetime


def age(begin, end):
    """
    calculates the number of full years between begin and end
    """
    return end.year - begin.year # - ((end.month, end.day) < (begin.month, begin.day))


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


# summarize response attributes by Response #
# pivot_table excludes records if any of these cols are null, such as the DoB
df_r = df.drop_duplicates(subset='Response')[[c for c in df.columns if c not in ['Question Number', 'Answer']]]


# pivot questions by Response # and merge back to the attributes
df_p = df.pivot_table(index=['Response'], values='Answer', columns='Question Number', aggfunc='first')\
         .reset_index()\
       .merge(df_r, how='inner', on='Response')


# rename the columns
#     I chose to pivot using the numeric column names vs. merging the question list, because it would 
#     save memory for a large dataset vs. repeating the question for every row.
question_dict = {n : q for n, q in zip(df_q['Number'], df_q['Question'])}
df_p.columns = [question_dict.get(c, c) for c in df_p.columns]


# clean date and time, create Completion Date column
df_p['Date'] = to_datetime(df_p['What day did you fill the survey in?'],
                           dayfirst=True, errors='coerce')

df_p['Date'] = where(df_p['Date'].isna(), 
                     to_datetime(df_p['What day did you fill the survey in?']
                               .str.replace('.* - (.*)', '\\1 ' + str(CURRENT_DATE.year), regex=True)),
                     df_p['Date'])
    
df_p[['Hour', 'Minute', 'AMPM']] = df_p['What time did you fill the survey in?']\
                                       .str.replace('.', ':', regex=False)\
                                       .str.extract('(\d{1,2}):?(\d{2})\s?(.*)')
    
df_p['Hour'] = df_p['Hour'].astype(int) + where(df_p['AMPM'].str.lower().str.contains('pm'), 12, 0)
df_p['Minute'] = df_p['Minute'].astype(int)

df_p['Completion Date'] = df_p['Date']\
                          + to_timedelta(df_p['Hour'], unit='h')\
                          + to_timedelta(df_p['Minute'], unit='m')


# understand the age of the customer based on their Date of Birth (DoB)
df_p['Age of Customer'] = df_p['DoB'].apply(lambda x: age(x, CURRENT_DATE))


# remove any answers that are not a customer's first or latest
group_cols = ['Name', 'Store', 'Country']
df_p['Result'] = where(df_p['Completion Date'] == df_p.groupby(group_cols)['Completion Date'].transform('min'),
                       'First',
                       where(df_p['Completion Date'] == df_p.groupby(group_cols)['Completion Date'].transform('max'),
                             'Latest', 'Other'))
df_p = df_p.loc[df_p['Result'] != 'Other']


# classify NPS recommendation
score_field = 'Would you recommend C&BSco to your friends and family? (Score 0-10)'
df_p['Detractor'] = where(df_p[score_field].astype(int) <= 6, 1, nan)
df_p['Passive'] = where((df_p[score_field].astype(int) >= 7) 
                        & (df_p[score_field].astype(int) <= 8), 1, nan)
df_p['Promoter'] = where(df_p[score_field].astype(int) > 8, 1, nan)


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
 