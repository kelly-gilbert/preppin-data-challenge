# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 12 - Regulatory Reporting Alignment
https://preppindata.blogspot.com/2023/03/2023-week-12-regulatory-reporting.html

- Input the data
- Fill down the years and create a date field for the UK bank holidays
- Combine with the UK New Customer dataset
- Create a Reporting Day flag
  - UK bank holidays are not reporting days
  - Weekends are not reporting days
- For non-reporting days, assign the customers to the next reporting day
- Calculate the reporting month, as per the definition above ("...any customers joining on that last 
  working day will actually be counted in the following month")
- Filter our January 2024 dates
- Calculate the reporting day, defined as the order of days in the reporting month
  - You'll notice reporting months often have different numbers of days!
- Now let's focus on ROI data. This has already been through a similar process to the above, but 
  using the ROI bank holidays. We'll have to align it with the UK reporting schedule
- Rename fields so it's clear which fields are ROI and which are UK
- Combine with UK data
- For days which do not align, find the next UK reporting day and assign new customers to that day 
  (for more detail, refer to the above description of the challenge)
- Make sure null customer values are replaced with 0's
- Create a flag to find which dates have differing reporting months when using the ROI/UK systems
- Output the data

Author: Kelly Gilbert
Created: 2023-03-22
Requirements:
  - input dataset:
      - New Customer Reporting.xlsx
  - output dataset (for results check only):
      - New Customers Ready to Report.csv
"""


from numpy import busday_count, busday_offset, NaN, where
import pandas as pd
from pandas.tseries.offsets import MonthEnd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def first_rept_day_of_month(dates, holidays=[]):
    """
    for a series of dates, return the first reporting day of that month, which is the
    last business day of the previous month
    """

    return busday_offset(dates.values.astype('datetime64[M]'),
                         offsets=-1,
                         roll='forward',
                         holidays=holidays)


def last_bus_day_of_month(dates, holidays=[]):
    """
    for a series of dates, return the last business day of that month
    """

    return busday_offset((dates + MonthEnd(0)).values.astype('datetime64[D]'),
                         offsets=0,
                         roll='backward',
                         holidays=holidays)


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\New Customer Reporting.xlsx') as xl:
    df_uk_hol = pd.read_excel(xl, sheet_name='UK Bank Holidays')
    df_uk = pd.read_excel(xl, sheet_name='New Customers')
    df_roi = ( pd.read_excel(xl, sheet_name='ROI New Customers')
                 .rename(columns={'New Customers' : 'ROI New Customers',
                                  'Reporting Month' : 'ROI Reporting Month',
                                  'Reporting Date' : 'Date' }) )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# clean UK holiday data (fill down year and convert to date)
holidays = ( pd.to_datetime(df_uk_hol['Year'].ffill().astype('Int64').astype(str) 
                            + df_uk_hol['Date'].dt.strftime('-%m-%d'))
               .values.astype('datetime64[D]') )


# join UK and ROI data on the date
df_all = df_uk.merge(df_roi,
                     how='outer',
                     on='Date')


# find the UK reporting date, adjusted for UK holidays and weekends
df_all['Reporting Date'] = busday_offset(df_all['Date'].values.astype('datetime64[D]'), 
                                         offsets=0,
                                         roll='forward',
                                         holidays=holidays)


# sum UK and ROI customers by reporting date
df_all = ( df_all.groupby('Reporting Date', as_index=False)
                 .agg(ROI_Reporting_Month = ('ROI Reporting Month', 'max'),
                      New_Customers = ('New Customers', 'sum'),
                      ROI_New_Customers = ('ROI New Customers', 'sum'))
                 .rename(columns=lambda c: c.replace('_', ' ')) )


# find the UK reporting month (if it is the last business day of the month --> next month)
df_all['Reporting Month'] = where((df_all['Reporting Date'] 
                                       == last_bus_day_of_month(df_all['Reporting Date'],
                                                                holidays=holidays)),
                                  (df_all['Reporting Date'] 
                                       + pd.DateOffset(months=1)).values.astype('datetime64[M]'),
                                  df_all['Reporting Date'].values.astype('datetime64[M]'))


# remove 2024 reporting months
df_all = df_all.loc[df_all['Reporting Month'].dt.year <= 2023]


# add the ROI vs UK month misalignment flag
df_all['Misalignment Flag'] = where(df_all['Reporting Month'] == df_all['ROI Reporting Month'],
                                    NaN,
                                    'X')


# find the reporting day of month
df_all['Reporting Day'] = busday_count(
                              first_rept_day_of_month(df_all['Reporting Month'], holidays=holidays),
                              df_all['Reporting Date'].values.astype('datetime64[D]'),
                              holidays=holidays
                          ) + 1


# format the dates
df_all['Reporting Date'] = df_all['Reporting Date'].dt.strftime('%d/%m/%Y')
df_all['Reporting Month'] = df_all['Reporting Month'].dt.strftime('%B-%Y')
df_all['ROI Reporting Month'] = ( df_all['ROI Reporting Month'].dt.strftime('%b-%y')
                                                               .str.replace('Sep', 'Sept', regex=False))


# fill zeroes
df_all[['New Customers', 'ROI New Customers']] = df_all[['New Customers', 'ROI New Customers']].fillna(0)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_all.to_csv(r'.\outputs\output-2023-12.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\New Customers Ready to Report.csv']
my_files = [r'.\outputs\output-2023-12.csv']
unique_cols = [['Reporting Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)




#---------------------------------------------------------------------------------------------------
# testing options for converting the holiday dates to the correct year
#---------------------------------------------------------------------------------------------------

# import random as rnd


# # make 1 million records
# df_test = pd.DataFrame({'Date' : 
#                         rnd.choices(pd.date_range('1900-01-01', '2250-12-31', freq='1D'), 
#                                     k=200_000)})
# df_test['Year'] = rnd.choices([2022, 2023], k=200_000)



# # option 1: string replace (awkward handling of leap years)
# # 1 s ± 18.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) -- FASTER

# %%timeit 
# df_test['Date2'] = where((df_test['Date'].dt.month==2) & (df_test['Date'].dt.day==29),
#                           pd.to_datetime(df_test['Year'].astype(str) + '-02-28'),
#                           pd.to_datetime(df_test['Year'].astype(str) + df_test['Date'].dt.strftime('-%m-%d'), errors='coerce'))
 
    
# # option 2: replace (doesn't handle leap years)

# %%timeit 
# df_test['Date3'] = [d.replace(year = y) for d, y in zip(df_test['Date'], df_test['Year'])]

# pd.testing.assert_series_equal(df_test['Date2'], 
#                                df_test['Date3'], 
#                                check_datetimelike_compat=True,
#                                check_names=False)   


# # option 3: offset (SLOW)
# # 6.44 s ± 97.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

# %%timeit 
# df_test['Date4'] = [d + pd.DateOffset(year=y) for d, y in zip(df_test['Date'], df_test['Year'])]

# pd.testing.assert_series_equal(df_test['Date2'], 
#                                df_test['Date4'], 
#                                check_datetimelike_compat=True,
#                                check_names=False)    
