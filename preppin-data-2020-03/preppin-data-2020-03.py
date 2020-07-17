# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-04
https://preppindata.blogspot.com/2020/01/2020-week-4.html
 
De-duplicating survey data

- Input the data
- Change the Question Number for the question asked
- Clean the Country and Store names
  We only want English names for places
- Clean up the dates and times to create a 'Completion Date' as a Date Time field
- Understand the age of the customer based on their Date of Birth (DoB)
  Nulls are ok
  Their age is taken to the date of 22nd January 2020
- Find the first answer for each customer in each store and country
- Find the latest answer for each customer in each store and country (if there are multiple responses)
- Remove any answers that are not a customer's first or latest
- Classify the 'NPS Recommendation' question based on the standard logic:
  0-6 makes the customer a 'Detractor'
  7-8 makes the customer a 'Passive' 
  9-10 makes the customer a 'Promoter'
- Output the data

Author: Kelly Gilbert
Created: 2020-07-05
Requirements: input dataset
  - PD 2020 Wk 4 Input.csv
"""

from os import chdir
from pandas import read_csv, pivot_table


#------------------------------------------------------------------------------
# import and explore the data
#------------------------------------------------------------------------------

# import the data
chdir('C:\\projects\\preppin-data-challenge\\preppin-data-2020-04')

df = read_csv('.\\inputs\\PD 2020 Wk 4 Input.csv', 
              parse_dates=['DoB'], infer_datetime_format=True, dayfirst=True)

# read questions into a series
s_questions = read_csv('.\\inputs\\Store Survey Results - Question Sheet.csv', index_col=['Number'], squeeze=True)


# what are the questions?
s_questions

# explore the answer data -- we have one row per response/question
df.dtypes
df.describe(include='all')

# what are the different date formats? (what type of cleaning will we need?)
df[df['Question Number']=='1'].groupby('Answer')['Question Number'].count()

# what are the different time formats?
df[df['Question Number']=='2'].groupby('Answer')['Question Number'].count()


#------------------------------------------------------------------------------
# reshape the data with questions in columns
#-----------------------------------------------------------------------------

df2 = pivot_table(df, values='Answer', index=['Response', 'Country', 'Store', 'Name', 'DoB'],
                    columns=['Question Number'], aggfunc=min, fill_value=nan)

# rename the columns with the question text
df2.rename(columns=s_questions.to_dict(), inplace=True)


#------------------------------------------------------------------------------
# clean the date and time columns
#-----------------------------------------------------------------------------

# dd/mm/yyyy
# d/m/yyyy
# yyyy-mm-dd
# yyyy/mm/dd
# ddth mmm yyyy
# d mmm yyyy
# ddd - dth mmm
#
from pandas import to_datetime

df2
df2['dc'] = to_datetime(df2['What day did you fill the survey in?'], errors='coerce', dayfirst=True)
df2[['What day did you fill the survey in?','dc']]

df2[df2['dc'].isnull()]



def clean_datetime(col):
    # attempt to clean using pandas to_datetime
    col2 = to_datetime(col, errors='coerce', dayfirst=True)
    
    # if any were skipped...
    if len(col2[col2.isnull()]) > 0:
        print(col2[col2.isnull()][[0,0]]) 
        
        
    return col2

clean_datetime(df2['What day did you fill the survey in?'])

col = df2['What day did you fill the survey in?']
type(col)


df2.columns

df.head()
df['Question Number'].unique()

df.groupby(['Question Number', 'Answer']).count()

df[df['Question Number'].unique()


df[df['Question Number']=='1']['Answer'].unique()


df_questions.head()
df.columns


df[df['Question Number']=='1']['Answer'].unique()

print(dates)

# import the team info and correct spelling of Division
df_team = xl.parse('Team List')
df_team.rename(columns = {'Divison':'Division'}, inplace = True)


# concatenate the results sheets
result_sheets = [s for s in xl.sheet_names if 'Results' in s]
df = None
for sheet in result_sheets:
    df = concat([df, xl.parse(sheet)])


# keep necessary columns, remove future games, identify winner/loser
df = df[['Date', 'Visitor/Neutral', 'PTS', 'Home/Neutral', 'PTS.1']]
df = df[df['PTS'].notna()]
df['winner'] = where(df['PTS']>=df['PTS.1'], df['Visitor/Neutral'], df['Home/Neutral'])
df['loser'] = where(df['PTS']>=df['PTS.1'], df['Home/Neutral'], df['Visitor/Neutral'])


# convert date
df['Date'] = [dt.strptime(d, '%a %b %d %Y') for d in df['Date']]


# add the conferences
df = df.merge(df_team, left_on='winner', right_on='Team', how='left') \
     .drop(columns=['Team','Division'])
df = df.merge(df_team, left_on='loser', right_on='Team', how='left', 
              suffixes=('_winner', '_loser')).drop(columns=['Team','Division'])
df['in_conference'] = where(df['Conference_winner']==df['Conference_loser'], 1, 0)


# put winner/loser into separate rows
id_vars = ['Date', 'Home/Neutral', 'Visitor/Neutral', 
           'Conference_winner', 'Conference_loser', 'in_conference']
df = melt(df, id_vars=id_vars,  value_vars=['winner', 'loser'], 
          var_name='team_type', value_name='Team')
df['conference'] = where(df['team_type']=='winner', df['Conference_winner'], df['Conference_loser'])
df.drop(columns=['Conference_winner', 'Conference_loser'], inplace=True)


# flags for summarization
df['home_flag'] = where(df['Team']==df['Home/Neutral'], 1, 0)
df['away_flag'] = where(df['Team']==df['Visitor/Neutral'], 1, 0)

df['win_flag'] = where(df['team_type']=='winner', 1, nan)
df['loss_flag'] = where(df['team_type']=='loser', 1, nan)

df.sort_values(['Team', 'Date'], ascending=False, inplace=True)
df['win_streak'] = df.groupby('Team')['win_flag'].cumsum(skipna=False) # this will count up from one until it hits a NaN
df['loss_streak'] = df.groupby('Team')['loss_flag'].cumsum(skipna=False)

df['win_flag'] = df['win_flag'].fillna(0)
df['loss_flag'] = df['loss_flag'].fillna(0)

df['conference_win_flag'] = where((df['team_type']=='winner') & (df['in_conference']==1), 1, 0)
df['conference_loss_flag'] = where((df['team_type']=='loser') & (df['in_conference']==1), 1, 0)

df['home_win_flag'] = where((df['team_type']=='winner') & (df['home_flag']==1), 1, 0)
df['home_loss_flag'] = where((df['team_type']=='loser') & (df['home_flag']==1), 1, 0)

df['away_win_flag'] = where((df['team_type']=='winner') & (df['away_flag']==1), 1, 0)
df['away_loss_flag'] = where((df['team_type']=='loser') & (df['away_flag']==1), 1, 0)

df['date_rank'] = df.groupby('Team')['Date'].rank(method='first', ascending=False)
df['L10_win_flag'] = where((df['team_type']=='winner') & (df['date_rank']<=10), 1, 0)
df['L10_loss_flag'] = where((df['team_type']=='loser') & (df['date_rank']<=10), 1, 0)


# summarize by team
df_summary = df.groupby(['conference','Team'], as_index=False).agg( 
               { 'win_flag' : {'W' : 'sum'},
                 'loss_flag' : {'L' : 'sum'},
                 'conference_win_flag' : {'Conf_W' : 'sum'},
                 'conference_loss_flag' : {'Conf_L' : 'sum'},
                 'home_win_flag' : {'Home_W' : 'sum'},
                 'home_loss_flag' : {'Home_L' : 'sum'},
                 'away_win_flag' : {'Away_W' : 'sum'},
                 'away_loss_flag' : {'Away_L' : 'sum'},
                 'L10_win_flag' : {'L10_W' : 'sum'},
                 'L10_loss_flag' : {'L10_L' : 'sum'},
                 'win_streak' : {'Strk_W' : 'max'},
                 'loss_streak' : {'Strk_L' : 'max'}
               }
             )

# remove the extra column index level and convert numbers to integer
df_summary.columns = [c[0] if c[1]=='' else c[1] for c in df_summary.columns]
df_summary = concat([df_summary[['conference','Team']], 
                     df_summary.iloc[:, 2:].fillna(0).astype(int)], axis=1)


# calculations
df_summary['Pct'] = (df_summary['W'] / (df_summary['W'] + df_summary['L'])).round(3)
df_summary['Conf'] = df_summary['Conf_W'].astype(str) + '-' + df_summary['Conf_L'].astype(str)
df_summary['Home'] = df_summary['Home_W'].astype(str) + '-' + df_summary['Home_L'].astype(str)
df_summary['Away'] = df_summary['Away_W'].astype(str) + '-' + df_summary['Away_L'].astype(str)
df_summary['L10'] = df_summary['L10_W'].astype(str) + '-' + df_summary['L10_L'].astype(str)
df_summary['Strk'] = where(df_summary['Strk_W']==0, 'L' + df_summary['Strk_L'].astype(str), 
                                                    'W' + df_summary['Strk_W'].astype(str))

# conference rank
df_summary['Rank'] = df_summary.groupby('conference')['Pct'].rank(method='max', ascending=False)
df_summary.sort_values(['conference', 'Rank'], ascending=True, inplace=True)
    # the provided output isn't sorted

# output one sheet per conference
cols = ['Rank', 'Team', 'W', 'L', 'Pct', 'Conf', 'Home', 'Away', 'L10', 'Strk']
writer = ExcelWriter(r'.\outputs\output-2020-03.xlsx', engine='xlsxwriter')

for c in df_summary['conference'].unique():
    df_summary[df_summary['conference']==c].to_excel(writer, columns=cols,  
                                                     sheet_name=c + 'ConferenceStandings', 
                                                     index = False)
writer.save()

#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

# read in the solution file
xl = ExcelFile(r'.\outputs\ExampleOutputs.xlsx')
df_solution = xl.parse(parse_dates=False, converters={'Away': str})

# read in my file
xl = ExcelFile(r'.\outputs\output-2020-03.xlsx')
df_mine = xl.parse(parse_date=False)


# compare
df_compare = df_solution.merge(df_mine, how='outer', on=None)

if 'Team_x' in df_compare or 'Team_y' in df_compare:
    print(str(len(df_compare[df_compare['Team_y'].isna()])) + ' records in solution, not in mine' \
      + '\n' \
      + str(len(df_compare[df_compare['Team_x'].isna()])) + ' records in mine, not in solution'
     )
elif len(df_solution.columns) != len(df_mine.columns) or \
    df_solution.columns != df_mine.columns:
    print('Columns do not match')
    print('Solution columns: ')
    print(df_solution.columns)
    print('My columns: ')
    print(df_mine.columns)
else:
    print('All records match')
