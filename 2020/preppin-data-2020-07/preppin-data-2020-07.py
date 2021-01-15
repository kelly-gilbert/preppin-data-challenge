# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-07
https://preppindata.blogspot.com/2020/01/2020-week-7.html
 
Summarize employee data

- Input Data
- Create a full list of employees
- Create an end date for current employees (1st March 2020)
- Create a scaffold month that can have the Employee data joined on to it
- Form your measures for analysis:
  - Count number of employees in employment by the company that month.
  - If the employee leaves in that month, remove them from the reporting within 
    the month of leaving.
  - Avg Salary per employee per month
  - Total Salary paid by the company per month
- Output the data

Author: Kelly Gilbert
Created: 2020-02-15
Requirements: input datasets
  - PD 2020 Wk 7 Current Employees Input.csv
  - PD 2020 Wk 7 Leavers Input.csv
  - PD 2020 Wk 7 Reporting Date Input.csv
"""

from pandas import read_csv, concat
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta


# read in the files
df_curr = read_csv('.\\inputs\\PD 2020 Wk 7 Current Employees Input.csv')
df_left = read_csv('.\\inputs\\PD 2020 Wk 7 Leavers Input.csv')
df_dates = read_csv('.\\inputs\\PD 2020 Wk 7 Reporting Date Input.csv')#


# prepare the current employees data:
# remove non-numeric chars from salary, add the leave month
df_curr['Salary'] = df_curr['Salary'].str.replace(r"[\D]",'')  
df_curr['Salary'] = df_curr['Salary'].astype(int)
df_curr['Leave Date'] = '3/1/2020'


# concatenate (union) the current and left employees
df_all = concat([df_curr, df_left], sort=False)


# convert the join/leave dates to the first of the month for joining
df_all['Join Month'] = [parse(d) for d in df_all['Join Date'].str.replace('/\d+/', '/1/')]
df_all['Leave Month'] = [parse(d) for d in df_all['Leave Date'].str.replace('/\d+/', '/1/')]


# convert the date inputs to the first of the month for joining
df_dates['Month'] = [parse(d) + relativedelta(day=1) for d in df_dates['Month']]


# add fields for join, then merge the dataframes to create a cross join
df_all['Link'] = 1
df_dates['Link'] = 1
df_all = df_all.merge(df_dates, left_on='Link', right_on='Link')


# remove report dates outside of the employee's range
date_in_range = (df_all['Month'] >= df_all['Join Month']) \
                 & (df_all['Month'] < df_all['Leave Month'])
df_all = df_all[date_in_range]


# summarize
df_summary = df_all.groupby('Month', as_index=False).agg( 
        { 'Employee ID' : 'count' , 
         'Salary': 'sum' }
        )

df_summary.columns = ['Month', 'Current Employees', 'Total Monthly Salary']
df_summary['Avg Salary per Current Employee'] = \
            df_summary['Total Monthly Salary'] / df_summary['Current Employees']


# output the file, reordering the columns to match the example output
df_summary.to_csv(path_or_buf='.\\outputs\\output-2020-07.csv', index=False, 
       columns = ['Total Monthly Salary', 'Month', 'Current Employees',
                  'Avg Salary per Current Employee'])