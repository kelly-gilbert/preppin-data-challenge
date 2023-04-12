# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 15 - Easter Dates
https://preppindata.blogspot.com/2023/04/2023-week-15-easter-dates.html

- Input the data
- Reshape it so that we have a list of Easter Sunday dates
- Filter the dataset so that we only have past dates
    - i.e. 1700 - 2023
- Output the data

Author: Kelly Gilbert
Created: 2023-04-12
Requirements:
  - input dataset:
      - easterdates.xls
  - output dataset (for results check only):
      - Easters.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_excel(r'.\inputs\easterdates.xls')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# reshape the month/day headers into two columns
df_headers = ( df.iloc[-2:].T
                 .set_axis(['day', 'month'], axis=1)
                 .query("day == day")
                 .assign(month = lambda df_x: df_x['month'].str.replace(' ', ''),
                         day = lambda df_x: df_x['day'].astype(int))
                 .ffill() )


# reshape the years into one column and join them to the month/days
df_easters = ( df.iloc[:-2]
                 .melt(var_name='col_name', value_name='year')
                 .assign(year = lambda df_x: pd.to_numeric(df_x['year'], errors='coerce'))
                 .query("year == year & year <= 2023")
                 .merge(df_headers,
                        how='inner',
                        left_on='col_name',
                        right_index=True) )


# construct the date and add the year rank
df_easters['Easter Sunday'] = ( pd.DatetimeIndex(df_easters['month'] + ' '
                                                    + df_easters['day'].astype(str) + ', '
                                                    + df_easters['year'].astype(int).astype(str))
                                     .to_period('D') 
                                     .astype('datetime64[D]') )

df_easters['Calculation1'] = df_easters['year'].rank().astype(int)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_easters.to_csv(r'.\outputs\output-2023-15.csv',
                  index=False, 
                  columns=['Calculation1', 'Easter Sunday'],
                  date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Easters.csv']
my_files = [r'.\outputs\output-2023-15.csv']
unique_cols = [['Calculation1']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
