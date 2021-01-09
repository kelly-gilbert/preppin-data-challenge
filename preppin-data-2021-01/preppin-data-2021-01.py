# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2021-01
https://preppindata.blogspot.com/2021/01/2021-week-1.html
 
Data cleaning

- Connect and load the csv file (help)
- Split the 'Store-Bike' field into 'Store' and 'Bike' (help)
- Clean up the 'Bike' field to leave just three values in the 'Bike' field (Mountain, Gravel, Road) (help)
- Create two different cuts of the date field: 'quarter' and 'day of month' (help)
- Remove the first 10 orders as they are test values (help)
- Output the data as a csv (help)

Author: Kelly Gilbert
Created: 2021-01-09
Requirements: 
  - input dataset (PD 2021 Wk 1 Input - Bike Sales.csv)
  - output dataset (for results check, PD 2021 Wk 1 Output.csv)
  
"""

from os import chdir
from pandas import merge, read_csv


# connect and load the csv file
chdir('C:\\projects\\preppin-data-challenge\\preppin-data-2021-01')

df = read_csv('.\\inputs\\PD 2021 Wk 1 Input - Bike Sales.csv', 
              parse_dates=['Date'])
#df.info()


# split the 'Store-Bike' field into 'Store' and 'Bike'
df[['Store','Bike']] = df['Store - Bike'].str.split(pat=' - ', expand=True)

# view the list of values for the new fields
#df['Store'].unique()
#df['Bike'].unique()


# clean up the 'Bike' field to leave just three values in the 'Bike' field 
# (Mountain, Gravel, Road)
remap = { 'Graval' : 'Gravel',
          'Gravle' : 'Gravel',
          'Mountaen' : 'Mountain',
          'Rood' : 'Road',
          'Rowd' : 'Road' }

df['Bike'].replace(remap, inplace=True)

# check the new values
#df['Bike'].unique()


# create two different cuts of the date field: 'quarter' and 'day of month'
df['Quarter'] = df['Date'].dt.quarter
df['Day of Month'] = df['Date'].dt.day
#df[['Date', 'Quarter', 'Day of Month']]  


# remove the first 10 orders as they are test values
df = df.iloc[10:]


# output the data as a csv
col_order = ['Quarter', 'Store', 'Bike', 'Order ID', 'Customer Age',
             'Bike Value', 'Existing Customer?', 'Day of Month']
df[col_order].to_csv('.\\outputs\\output-2021-01.csv', index=False)


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

# read in the solution file
df_solution = read_csv('.\\outputs\\PD 2021 Wk 1 Output.csv')

# read in my file
df_mine = df_solution = read_csv('.\\outputs\\output-2021-01.csv')

# are the fields the same and in the same order?
if list(df_solution.columns) != list(df_mine.columns):
    print('*** Columns do not match ***')
    print('    Columns in solution: ' + str(list(df_solution.columns)))
    print('    Columns in mine    : ' + str(list(df_mine.columns)))


# are the values the same?
df_solution['check'] = 1
df_mine['check'] = 1
df_compare = df_solution.merge(df_mine, how='outer', 
                               on=list(df_solution.columns)[:-1])

if df_compare['check_x'].count() != len(df_compare):
    print('*** Values do not match ***')
    print(df_compare[df_compare['check_x'] != df_compare['check_y']])