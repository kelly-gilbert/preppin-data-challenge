# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 48 - Reporting Week Calendars (polars)
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
Created: 2023-12-02
Requirements:
  - input dataset:
      - Year Input.csv
  - output dataset (for results check only):
      - 2023 Reporting Dates.csv
"""


from datetime import date, timedelta
import polars as pl
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
        return date(year, 2, 1) - date(year, 2, 1).weekday() * timedelta(days=1)
    else:
        raise ValueError('Year argument must be numeric.')


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

# input the year from the file
year = int(pl.read_csv(r'.\inputs\Year Input.csv', try_parse_dates=True)[0, 0])


# get beginning of year dates
boy = get_boy(year)
boy_ly = get_boy(year-1)


# generate all dates in the specified range
df = ( pl.LazyFrame()
         .with_columns(
             pl.date_range(start=date(year, 1, 1),
                           end=date(year, 12, 31),
                           interval='1d')
               .alias('Calendar Date')
         )
         .with_columns(
             pl.when(pl.col('Calendar Date') >= boy) 
               .then(boy)
               .otherwise(boy_ly)
               .alias('boy')
         )
         .with_columns( 
             ((pl.col('Calendar Date') - pl.col('boy')).dt.days() + 1).alias('Reporting Day')
         )
         .with_columns(
             pl.col('boy').dt.year().alias('Reporting Year'),
             ((pl.col('Reporting Day') - 1) // 28 + 1).alias('Reporting Month'),
             ((pl.col('Reporting Day') - 1) // 7 + 1).alias('Reporting Week')

         )
     )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

( df.collect()
    .select(pl.all().exclude('boy'))
    .write_csv(fr'.\outputs\output-{year} Reporting Dates2.csv', 
               datetime_format='%d/%m/%Y') )


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
