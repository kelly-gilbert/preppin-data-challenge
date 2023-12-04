# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 48 - Reporting Week Calendars
https://preppindata.blogspot.com/2023/11/2023-week-48-reporting-week-calendars.html


Their reporting year begins on the Monday before 1st February
e.g. In 2023, 1st February fell on a Wednesday. Therefore the first day of the reporting year will be 30th January
Each Reporting Month contains exactly 4 Reporting Weeks

- Input the data
- Create a way for the user to choose which calendar year they want to get the reporting dates for
- Make sure to have a row for each date in the selected year
- Create a field for the Reporting Year (based off the above logic)
- Create a field for the Reporting Day
  - Day 1 will be the Monday before the 1st Feb
- Create a field for the Reporting Week
- Create a field for the Reporting Month
  - Each month contains exactly 4 weeks
- Output the data, naming the file according to calendar year selected when the workflow runs

Author: Kelly Gilbert
Created: 2023-11-30
Requirements:
  - input dataset:
      - Year Input.csv
  - output dataset (for results check only):
      - 2023 Reporting Dates.csv
"""


from datetime import datetime, timedelta
from numpy import where
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def get_boy(year):
    """
    returns the beginning-of-year date for a given year, where beginning of year is the monday
    of the week that contains Feb 1
    """
    
    if isinstance(year, int) or isinstance(year, float):
        return datetime(year, 2, 1) - datetime(year, 2, 1).weekday() * timedelta(days=1)
    else:
        raise ValueError('Year argument must be numeric.')


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

# input the year from the file
year = int(pd.read_csv(r'.\inputs\Year Input.csv', dayfirst=True).iloc[0, 0])


# generate all dates in the specified range
df = pd.DataFrame({ 'Calendar Date' : pd.date_range(start=datetime(year, 1, 1),
                                                    end=datetime(year, 12, 31),
                                                    freq='1D') })

# get beginning of year dates
boy = get_boy(year)
boy_ly = get_boy(year-1)


# calc date parts
df['boy'] = where(df['Calendar Date'] >= boy, pd.to_datetime(boy), pd.to_datetime(boy_ly))

df['Reporting Year'] = df['boy'].dt.year
df['Reporting Day'] = (df['Calendar Date'] - df['boy']).dt.days + 1
df['Reporting Month'] = (df['Reporting Day'] - 1) // 28 + 1 
df['Reporting Week'] = (df['Reporting Day'] - 1) // 7 + 1 


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(fr'.\outputs\output-{year} Reporting Dates.csv', 
          columns=[c for c in df if c not in['boy']],
          index=False,
          date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2023 Reporting Dates.csv']
my_files = [r'.\outputs\output-2023 Reporting Dates.csv']
unique_cols = [['Calendar Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
