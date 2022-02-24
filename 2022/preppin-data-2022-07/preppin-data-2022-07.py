# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 07 - Call Center Agent Metrics
https://preppindata.blogspot.com/2022/02/2022-week-7-call-center-agent-metrics.html

- Input the data
- People, Location, Leader, and Dates:
    - Join the People, Location, and Leader data sets together
    - Remove the location id fields, the secondary leader id field
    - Create last name, first name fields for the agent and the leader
    - Limit the dates to just 2021 and join those to the People, Location, Leader step
    - Keep the id, agent name, leader 1, leader name, month start date, join, and location field
- Monthly Data
    - union the worksheets in the input step
    - merge the mismatched fields
    - create a month start date
    - remove the table names and file paths field
    - join the data with the people - remember we need to show every agent for every month
- Goals
    - add the goals input to the flow
    - clean the goal data to have the goal name & numeric value
    - add the goals to the combined people & data step
    - be sure that you aren't increasing the row count - the goals should be additional columns
- Metrics & Met Goal Flags
    - create a calculation for the percent of offered that weren't answered (for each agent, each month)
    - create a calculation for the average duration by agent (for each agent, each month)
    - create a calculation that determines if the sentiment score met the goal
    - create a calculation that determines if the not answered percent met the goal
- Output the data

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input dataset:
      - MetricData2021.xlsx
      - PeopleData.xlsx
  - output dataset (for results check only):
      - Call Center.csv
"""


from numpy import where, NaN
import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in the monthly metric sheets, add the Month Start Date, consolidate field names
with pd.ExcelFile(r'.\inputs\MetricData2021.xlsx') as xl:
    df_metric = pd.concat([pd.read_excel(xl, s)\
                               .assign(Month_Start_Date=pd.to_datetime(s + '1, 2021'))\
                               .rename(columns=lambda x: 'Calls ' + x 
                                                         if x in ['Offered', 'Not Answered', 'Answered']
                                                         else x)
                           for s in xl.sheet_names])


with pd.ExcelFile(r'.\inputs\PeopleData.xlsx') as xl:
    # read in the people data (join People, Leader, and Location tabs)
    df_people = pd.read_excel(xl, 'People')\
                  .merge(pd.read_excel(xl, 'Leaders'), left_on='Leader 1', right_on='id', 
                         how='left', suffixes=['', ' L'])\
                  .merge(pd.read_excel(xl, 'Location'), on='Location ID', how='left')\
                  .assign(Agent_Name=lambda df_x: df_x['last_name'] + ', ' + df_x['first_name'],
                          Leader_Name=lambda df_x: df_x['last_name L'] + ', ' + df_x['first_name L'])\
                  [['id', 'Agent_Name', 'Leader 1', 'Leader_Name', 'Location']]
        
 
    # read in and transpose the goal data, so goals are in columns    
    df_goals = pd.read_excel(xl, 'Goals')\
                 .assign(goal_amt=lambda df_x:df_x['Goals'].str.extract('.*? (?P<goal_amt>\d+)', expand=False)\
                                              .astype(float))\
                 .set_index('Goals')\
                 .T


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# generate all person/month combos, join metric and goal data
df_all = df_people.merge(pd.DataFrame({'Month_Start_Date' : df_metric['Month_Start_Date'].unique()}),
                         how='cross')\
                  .merge(df_metric, left_on=['id', 'Month_Start_Date'], 
                         right_on=['AgentID', 'Month_Start_Date'], how='left')\
                  .drop(columns='AgentID')\
                  .merge(df_goals, how='cross')
                  
                 
# create goal and summary calculations
df_all['Not Answered Rate'] = where(df_all['Calls Offered'].notna(),
                                    (df_all['Calls Not Answered'] / df_all['Calls Offered']).round(3),
                                    NaN)
df_all['Agent Avg Duration'] = where(df_all['Calls Offered'].notna(), 
                                     df_all['Total Duration'] / df_all['Calls Answered'], NaN).round(0)

# find the goal cols dynamically, since the name would change if the goal changed
not_answered_col = [c for c in df_goals.columns if 'Not Answered' in c][0]
sentiment_col = [c for c in df_goals.columns if 'Sentiment' in c][0]

df_all['Met Sentiment Goal'] = where(df_all['Sentiment'].notna(),
                                     df_all['Sentiment'] >= df_all[sentiment_col], NaN)
df_all['Met Not Answered Rate'] = where(df_all['Not Answered Rate'].notna(),
                                        df_all['Not Answered Rate'] < df_all[not_answered_col] / 100, NaN)                
                 

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_all.rename(columns=lambda x: x.replace('_', ' '))\
      .to_csv(r'.\outputs\output-2022-07.csv', index=False, date_format='%#d/%#m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

pd.set_option('display.width', 500)
pd.set_option('display.max_columns', 100)
pd.set_option('display.max_colwidth', 50)
#pd.set_option('display.column_space', 100)


solution_files = ['Call Center.csv']
my_files = ['output-2022-07.csv']
unique_cols = [['Month Start Date', 'id']]
col_order_matters = False
round_dec = 8

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_sol = pd.read_csv('.\\outputs\\' + solution_file)
    df_mine = pd.read_csv('.\\outputs\\' + my_files[i])

    # are the columns the same?
    solution_cols = list(df_sol.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_sol.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
        print('\n\n')
    else:
        print('Columns match\n')
        col_match = True


    # are the values the same? (only check if the columns matched)
    if col_match:
        errors = 0
        df_compare = df_sol.merge(df_mine, how='outer', on=unique_cols[i],
                                  suffixes=['_sol', '_mine'], indicator=True)
        
        # extra/missing records
        if len(df_compare[df_compare['_merge'] != 'both']) > 0:
            print('*** Missing or extra records ***\n')
            print('In solution, not in mine:\n')
            print(df_compare[df_compare['_merge'] == 'left_only'][unique_cols[i]])
            print('\n\nIn mine, not in solution:\n')
            print(df_compare[df_compare['_merge'] == 'right_only'][unique_cols[i]]) 
            print('\n')
            errors += 1

        # for the records that matched, check for mismatched values
        for c in [c for c in df_sol.columns if c not in unique_cols[i]]:
            if 'float' in df_compare[f'{c}_sol'].dtype.name:
                df_compare[f'{c}_sol'] = df_compare[f'{c}_sol'].round(round_dec)
                df_compare[f'{c}_mine'] = df_compare[f'{c}_mine'].round(round_dec)
                
            unmatched = df_compare[(df_compare['_merge']=='both')
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])
                                   & ((df_compare[f'{c}_sol'].notna()) 
                                       | (df_compare[f'{c}_mine'].notna()))]
            if len(unmatched) > 0:
                print(f'*** Values do not match: {c} ***\n')
                print(unmatched[unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                errors += 1
        
        if errors == 0:
            print('Values match')

    print('\n')  


# trickiest part this week was formatting the output with no leading zeroes in the day/month
# not specified in the instructions, but it appears that not answered rate should be rounded to 3 dec