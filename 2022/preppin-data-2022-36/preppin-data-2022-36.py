# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 36 - challenge title goes here
https://preppindata.blogspot.com/ - challenge url goes here

- Input the data
- The main challenge is to solve this using only employee_data input
- Create a Calendar Table
  - Create a date range for the calendar
    - This should be dynamic to handle new data
    - The start of the range should be the based on the year of the earliest date
      - If earliest date is 06/01/2021, the start date should be 01/01/2021
    - The end of the range should be the last day of the year for the latest date in the data set 
      - If the latest date is 06/01/2022, the end date should be 31/12/2022
  - Generate a row for every day between the start and end date to get a calendar table
- Create a field containing the full name for each employee
- Get a unique list of employees with their full name, first/last name fields, and employee id
- Join the list to the calendar table
  - You should have a table with one row per employee per day
- Join the new calendar table to the main table
  - One row per employee per day, even on days where the employee wasn’t scheduled
- Create a flag if the employee was scheduled on the day
- Handle any null values
- Output the data

Author: Kelly Gilbert
Created: 2022-09-07
Requirements:
  - input dataset:
      - employee_data.csv
  - output dataset (for results check only):
      - employee_calendar.csv
"""


from datetime import datetime
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\employee_data.csv', parse_dates=['scheduled_date'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# generate the date range
dates = pd.date_range(start=datetime(df['scheduled_date'].min().year, 1, 1), 
                      end=datetime(df['scheduled_date'].max().year, 12, 31), freq='1D')


# generate all possible combinations of employee/date, join to actual schedule, fill Nan with False
df_all = ( pd.DataFrame(dates, columns=['scheduled_date'])
             .merge(df.drop(columns='scheduled_date').drop_duplicates(), how='cross')
             .merge(df[['scheduled_date', 'emp_id']].assign(scheduled=True), 
                    on=['scheduled_date', 'emp_id'], how='left')
             .fillna(False)
         )


# add the full name
df_all.insert(loc=2, column='full_name', value=df_all['first_name'] + ' ' + df_all['last_name'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_all.to_csv(r'.\outputs\output-2022-36.csv', index=False, date_format='%#m/%#d/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\employee_calendar.csv']
my_files = [r'.\outputs\output-2022-36.csv']
unique_cols = [['scheduled_date', 'emp_id']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)






# --------------------------------------------------------------------------------------------------
# timing methods for adding the missing employee/date combos
# --------------------------------------------------------------------------------------------------

# make df larger by adding more dates and more employees
n = 200_000
df = pd.concat([df.assign(scheduled_date=df['scheduled_date'] - pd.DateOffset(months=12*(i % 10)),
                          emp_id=df['emp_id'] + (i//10)*20)
                for i in range(0,(n//len(df))+1)])

# n = 100_000 --> 2,670 unique dates, 150 unique employees --> 547,800 total combos
# n = 200_000 --> 2,670 unique dates, 300 unique employees --> 1,095,600 total combos





# method 1: pandas merge (cross join) -- FASTEST
# 500K records = 228 ms ± 11.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 1M records = 438 ms ± 29 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
df_all = ( pd.DataFrame(dates, columns=['scheduled_date'])
             .merge(df.drop(columns='scheduled_date').drop_duplicates(), how='cross')
             .merge(df[['scheduled_date', 'emp_id']].assign(scheduled=True), 
                    on=['scheduled_date', 'emp_id'], how='left')
         )


# SLOW
# method 2 - merge_ordered
# 500K records = 569 ms ± 3.17 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 1M records = 1.36 s ± 9.14 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit
df_all = ( pd.merge_ordered(pd.DataFrame(dates, columns=['scheduled_date']), 
                          df.assign(scheduled=True), right_by=['emp_id', 'first_name', 'last_name'])
             .merge(df.drop(columns='scheduled_date').drop_duplicates(), how='left', on='emp_id')
         )


# 2nd FASTEST
# method 3: convert the key cols to a multiIndex, then pad out the index with the missing combos
#           this version still needs to have the employee names added, but I didn't pursue it 
#           further because it was so much slower than the pure pandas approach
# 500K records = 451 ms ± 12.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 1M records = 904 ms ± 16.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
col_names = ['scheduled_date', 'emp_id']
new_idx = pd.MultiIndex.from_product([dates, df['emp_id'].unique()], names=col_names)
df_all = ( df[['scheduled_date', 'emp_id']].assign(scheduled=True)
             .set_index(col_names)
             .reindex(new_idx, fill_value=False)
             .reset_index()
         )


# ---------- non-pandas approaches ----------

# SLOW
# method 4: itertools product + merge
# 500K records = 605 ms ± 44 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 1M records = 1.26 s ± 170 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# the driver of the increased time is the conversion to a dataframe (creating the list of combos is fast)
%%timeit 
df_all = ( pd.DataFrame(product(dates, df['emp_id'].unique()), columns=['scheduled_date', 'emp_id'])
             .merge(df[['scheduled_date', 'emp_id']].assign(scheduled=True), 
                    on=['scheduled_date', 'emp_id'], how='left')
             .merge(df.drop(columns='scheduled_date').drop_duplicates(), how='left', on='emp_id')
         )


# SLOWEST
# method 5: use sets to construct a df of the missing combos (NOT scheduled), union to actual recs
#           (theoretically constructs a smaller df, since it's only the missing recs)
#           this version still needs to have the employee names added, but I didn't pursue it 
#           further because it was so much slower than the pure pandas approach
# 500K records = 985 ms ± 54.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 1M records = 2.1 s ± 64.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
df_all = ( pd.concat([pd.DataFrame(set(product(dates, df['emp_id'].unique())) 
                                   - set((df[['scheduled_date', 'emp_id']].itertuples(index=False))), 
                                   columns=['scheduled_date', 'emp_id']).assign(scheduled=False),
                                   df.assign(scheduled=True)])
         )



# --------------------------------------------------------------------------------------------------
# timing methods for adding the true/false flag
# --------------------------------------------------------------------------------------------------

# method 1 - pandas merge left + fillna -- FASTER
# 500K records = 245 ms ± 4.21 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 1M records = 478 ms ± 10.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
df_all = ( pd.DataFrame(dates, columns=['scheduled_date'])
             .merge(df.drop(columns='scheduled_date').drop_duplicates(), how='cross')
             .merge(df[['scheduled_date', 'emp_id']].assign(scheduled=True), 
                    on=['scheduled_date', 'emp_id'], how='left')
         )

df_all['scheduled'].fillna(False)


# method 2 - pandas merge left + merge indicator -- SLOWER
# 500K reords = 317 ms ± 42.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# 1M records = 599 ms ± 31.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
df_all = ( pd.DataFrame(dates, columns=['scheduled_date'])
             .merge(df.drop(columns='scheduled_date').drop_duplicates(), how='cross')
             .merge(df[['scheduled_date', 'emp_id']].assign(scheduled=True), 
                    on=['scheduled_date', 'emp_id'], how='left', indicator=True)
         )

df_all['scheduled'] = where(df_all['_merge']=='left_only', False, True)
