# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 28 - No sales today
https://preppindata.blogspot.com/2022/07/2022-week-28-c-no-sales-today.html

- Input the file
- Convert any data types required
- Create a new row for each day that doesn't have a sale
- Remove any date record where a sale occurred 
- Create a column for Day of the Week
- For each day of the week, count the numbers of dates where there were no sales
- Rename the count field as Number of Days
- Output the data

Author: Kelly Gilbert
Created: 2022-07-13
Requirements:
  - input dataset:
      - Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv
  - output dataset (for results check only):
      - PD 2022 Wk 28 Output.csv
"""


import pandas as pd
from output_check import output_check


# ---------- pandas method -------------------------------------------------------------------------

#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_sales = pd.read_csv(r".\inputs\Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv", 
                       parse_dates=['Sale Date'], dayfirst=True, usecols=['Sale Date'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# get a list of all possible dates
df_all = pd.DataFrame({ 'date' : pd.date_range(start=df_sales['Sale Date'].min(), 
                                               end=df_sales['Sale Date'].max(), freq='1D') })


# get dates that are in all dates, but not in sales
mask = ~df_all['date'].isin(df_sales['Sale Date'].unique())
df_missing = df_all.loc[mask, ['date']]


# get weekday name
df_missing['Day of the Week'] = df_missing['date'].dt.day_name()


# get counts by day of the week
df_out = ( df_missing['Day of the Week'].value_counts()
                     .reset_index()
                     .rename(columns={ 'Day of the Week' : 'Number of Days',
                                      'index' : 'Day of the Week'})
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-28.csv', index=False)





# ---------- non-pandas method ---------------------------------------------------------------------

from collections import Counter
from datetime import datetime
from numpy import datetime64


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_sales = pd.read_csv(r".\inputs\Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv", 
                       parse_dates=['Sale Date'], dayfirst=True, usecols=['Sale Date'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# days without sales
missing = list(set(pd.date_range(start=df_sales['Sale Date'].min(), 
                                 end=df_sales['Sale Date'].max(), freq='1D').values)
               -
               set(df_sales['Sale Date'].unique())
              )


# get days of the week
weekdays = [datetime64(d, 'D').astype(datetime).strftime('%A') for d in missing]


# get count by day of week
weekday_counts = Counter(weekdays)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

with open(r'.\outputs\output-2022-28.csv', 'w') as f:
    # write the headings
    f.write('Day of the Week,Number of Days\n')  

    # write out the data
    [f.write(f'{k},{v}\n') for k,v in weekday_counts.items()]




#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 28 Output.csv']
my_files = [r'.\outputs\output-2022-28.csv']
unique_cols = [['Day of the Week']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)




#---------------------------------------------------------------------------------------------------
# pandas method vs. sets method
#---------------------------------------------------------------------------------------------------

# pandas method:
# 1M recs = 26.1 ms ± 5.37 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

# sets method: -- slightly faster
# 1M recs = 19.1 ms ± 281 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)




#---------------------------------------------------------------------------------------------------
# options for finding dates with no sales
#---------------------------------------------------------------------------------------------------

# method 1: filter list
# 4,000 recs = 38.4 ms ± 810 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 1M recs    = 3.74 s ± 102 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
dates_wo_sales = list(filter(lambda x: x not in df['Sale Date'].unique(), 
                             list(pd.date_range(start=df['Sale Date'].min(), 
                                                end=df['Sale Date'].max(), freq='1D')))
                     )


# method 2: list comprehension
# 4,000 recs = 38.7 ms ± 1.4 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
# 1M recs    = 3.55 s ± 74.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
dates_wo_sales = [d for d 
                  in pd.date_range(start=df['Sale Date'].min(), end=df['Sale Date'].max(), freq='1D')
                  if d not in df['Sale Date'].unique()]


# method 3: sets -- FASTEST
# 4,000 recs = 1.19 ms ± 45.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each) -- FASTEST
# 1M recs    = 17.2 ms ± 1.03 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)

%%timeit 
dates_wo_sales = list(set(pd.date_range(start=df['Sale Date'].min(), end=df['Sale Date'].max(), freq='1D').values)
                      - set(df['Sale Date'].unique()))


# method 4: merge
# 4,000 recs = 7.12 ms ± 96.3 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 1M recs    = 214 ms ± 6.18 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit 
dates_wo_sales = ( df_all.merge(df_sales, left_on='date', right_on='Sale Date', 
                              how='left', indicator=True)
                         .query("_merge == 'left_only'") 
                 )



#---------------------------------------------------------------------------------------------------
# options for getting the weekday counts
#---------------------------------------------------------------------------------------------------

# all times similar at 1M recs

# method 1a: list comprehension and counter, weekday lookup
# 4,000 recs = 1.35 ms ± 79.3 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each)
# 1M res =     15.5 ms ± 993 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)

%%timeit 
dates_wo_sales = list(set(pd.date_range(start=df['Sale Date'].min(), end=df['Sale Date'].max(), freq='1D').values)
                      - set(df['Sale Date'].unique()))


day_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', '8']

weekdays = [day_names[datetime64(d, 'D').astype(datetime).weekday()] for d in dates_wo_sales]
weekday_counts = Counter()


# method 2: read into dataframe + value_counts
# 4,000 recs = 2.95 ms ± 66.1 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 1M recs =    18 ms ± 1.19 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)

%%timeit 
dates_wo_sales = list(set(pd.date_range(start=df['Sale Date'].min(), end=df['Sale Date'].max(), freq='1D').values)
                      - set(df['Sale Date'].unique()))

df_nosales = pd.DataFrame({'date' : dates_wo_sales})
df_nosales['Day of the Week'] = df_nosales['date'].dt.day_name()
weekday_counts = ( df_nosales['Day of the Week'].value_counts()
                  .reset_index()
                  .rename(columns={'Day of the Week':'Number of Days','index':'Day of the Week'})
                 )


# method 3: read into dataframe + groupby
# 4,000 recs = 5.53 ms ± 280 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 1M recs    = 20.4 ms ± 1.99 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)

%%timeit 
dates_wo_sales = list(set(pd.date_range(start=df['Sale Date'].min(), end=df['Sale Date'].max(), freq='1D').values)
                      - set(df['Sale Date'].unique()))

df_nosales = pd.DataFrame({'date' : dates_wo_sales})
df_nosales['Day of the Week'] = df_nosales['date'].dt.day_name()
weekday_counts = ( df_nosales.groupby('Day of the Week', as_index=False).agg(Number_of_Days=('date', 'count'))
                             .rename(columns=lambda x: x.replace('_', ' '))
                 )
