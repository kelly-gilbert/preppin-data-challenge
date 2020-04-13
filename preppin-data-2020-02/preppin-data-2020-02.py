"""
Preppin Data Challenge 2020-02
https://preppindata.blogspot.com/2020/01/2020-week-2.html
 
Cleaning date/time data
- Input Data
- Make the Time format suitable to fit the 24 hour clock
    - Factor in AM / PM
    - Ensure 12 am hour is captured correctly as 00:xx
- Remove unnecessary fields
- Output the data

Author: Kelly Gilbert
Created: 2020-02-18

Requirements: 
Input data - .\inputs\PD 2020 Wk 2 Input - Time Inputs.csv
"""

from os import chdir
from pandas import read_csv
from datetime import datetime as dt


# read in the file
chdir('C:\\projects\\preppin-data-challenge\\preppin-data-2020-02')
df = read_csv('.\\inputs\\PD 2020 Wk 2 Input - Time Inputs.csv')


# clean date field:
 
# convert the date from d/m/y to m/d/y
df['Date_out'] = [dt.strftime(dt.strptime(d, '%d/%m/%y'), '%m/%d/%Y') for d in df['Date']]


# clean time field:

# keep numeric characters and pad with zero
df['time_part'] = df['Time'].str.replace('\D','', regex=True)

# separate daypart into new column and add M if missing
df['am_pm'] = df['Time'].str.replace('([^amp]+)', '', regex=True, case=False)
df['am_pm'] = [t.ljust(2, 'm') if t != '' else '' for t in df['am_pm']]

# convert time to specified format
df['Time_out'] = [dt.strftime(
                         dt.strptime(t + p, '%I%M%p') if p!='' 
                         else dt.strptime(t, '%H%M'), '%H:%M'
                     )
                     for (t,p) in zip(df['time_part'],df['am_pm'])]


# final output

# combined date/time column
df['Date Time_out'] = df['Date_out'] + ' ' + df['Time_out'] + ':00'

df.to_csv('.\\outputs\\output-2020-02.csv', 
          columns = ['Date Time_out', 'Date_out', 'Time_out'],
          header = ['Date Time', 'Date', 'Time'],
          index = False)


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

df_solution = read_csv('.\\outputs\\PD 2020 Wk 2 Output.csv')
df_mine = read_csv('.\\outputs\\output-2020-02.csv')
df_compare = df_solution.merge(df_mine, how='outer', on='Date Time')


# print results
print(str(len(df_compare[df_compare['Date_x'].isna()])) + ' records in solution, not in mine' \
      + '\n' \
      + str(len(df_compare[df_compare['Date_x'].isna()])) + ' records in mine, not in solution'
     )