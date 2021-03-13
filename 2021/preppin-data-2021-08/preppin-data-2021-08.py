# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 8 - Karaoke Data
https://preppindata.blogspot.com/2021/02/2021-week-8-karaoke-data.html

Assumptions:
- Customers often don't sing the entire song
- Sessions last 60 minutes
- Customers arrive a maximum of 10 minutes before their sessions begin

- Input the data
- Calculate the time between songs
- If the time between songs is greater than (or equal to) 59 minutes, flag this as being a new session
- Create a session number field
- Number the songs in order for each session
- Match the customers to the correct session, based on their entry time
- The Customer ID field should be null if there were no customers who arrived 10 minutes (or less) before the start of the session
- Output the data

Author: Kelly Gilbert
Created: 2021-03-09
Requirements: 
  - pandas v 0.25.0 or higher
  - input dataset (Copy of Karaoke Dataset.xlsx)
  - output dataset (for results check):
    - Karaoke Output.csv
  
"""

from pandas import ExcelFile, merge, merge_asof, read_excel, Timedelta

# used for answer check only
from pandas import read_csv


def convert_id(customer_id):
    """convert long, numeric customer IDs to scientific notation to match the solution"""
    if len(customer_id) > 6 and customer_id.isnumeric():
        customer_id = "{:.2E}".format(float(customer_id)) 
    return customer_id


#--------------------------------------------------------------------------------
# input the data
#--------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Copy of Karaoke Dataset.xlsx') as xl:
    choices = read_excel(xl, 'Karaoke Choices').sort_values(by='Date')
    customers = read_excel(xl, 'Customers', converters={'Customer ID':str}).sort_values(by='Entry Time')


#--------------------------------------------------------------------------------
# process the data
#--------------------------------------------------------------------------------

# fix long customer IDs 
customers['Customer ID'] = [convert_id(c) for c in customers['Customer ID']]


# determine the session (if the time between songs is >= 59 minutes, increment the session)
choices['Session #'] = choices['Date'].diff(1).dt.total_seconds().ge(59*60).cumsum() + 1


# number the songs in order for each session
choices['Song Order'] = choices.groupby('Session #')['Date'].rank('dense', ascending=True).astype(int)


# join the customer to the closest session after their entry time, 10 min tolerance
session_start = choices[choices['Song Order']==1][['Date','Session #']]

customer_sessions = merge_asof(customers, session_start, left_on='Entry Time', right_on='Date', 
                               tolerance=Timedelta(minutes=10), direction='forward').dropna()


# join customer sessions to song list
final = merge(choices, customer_sessions, how='left', on=['Session #'], suffixes=['','_y'])
final.drop(columns=['Date_y'], inplace=True)


#--------------------------------------------------------------------------------
# output the file
#--------------------------------------------------------------------------------

final['Date'] = final['Date'].dt.round('1s')
final.to_csv('.\\outputs\\output-2021-08.csv', index=False, date_format='%d/%m/%Y %H:%M:%S',
             columns=['Session #', 'Customer ID', 'Song Order', 'Date', 'Artist', 'Song'])


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solutionFiles = ['Karaoke Output.csv']
myFiles = ['output-2021-08.csv']
col_order_matters = False

for i in range(len(solutionFiles)):
    print('---------- Checking \'' + solutionFiles[i] + '\' ----------\n')
    
    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solutionFiles[i])
    dfMine = read_csv('.\\outputs\\' + myFiles[i])
    
    # are the fields the same and in the same order?
    solutionCols = list(dfSolution.columns)
    myCols = list(dfMine.columns)
    if col_order_matters == False:
         solutionCols.sort()
         myCols.sort()

    col_match = False
    if solutionCols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(dfSolution.columns)))
        print('    Columns in mine    : ' + str(list(dfMine.columns)))
    else:
        print('Columns match\n')
        col_match = True
    
    # are the values the same? (only check if the columns matched)
    if col_match == True:
        dfSolution['join'] = 1
        dfMine['join'] = 1
        dfCompare = dfSolution.merge(dfMine, how='outer', on=list(dfSolution.columns)[:-1])
        dfCompare.rename(columns={'join_x':'in_solution', 'join_y':'in_mine'}, inplace=True)    
        
        if dfCompare['in_solution'].count() != len(dfCompare):
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')
    
    print('\n')