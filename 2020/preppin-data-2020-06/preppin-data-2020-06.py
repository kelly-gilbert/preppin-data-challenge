# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-06
https://preppindata.blogspot.com/2020/01/2020-week-6.html
 
- Input the data set
- Determine the best and worst GBP to USD exchange rates on a calendar week basis
- Take the Sales data and determine the UK / US Split
- Apply the UK / US sales split to the value sold in GBP
- For the calendar week US sales, determine:
  - What's the Maximum Sales value for US sales in USD
  - What's the Minimum Sales value for US sales in USD
  - What the weekly variance could be
- Output the data

Author: Kelly Gilbert
Created: 2020-02-16

Requirements:
  - input dataset: PD 2020 Wk 6 Input.xlsx
  - package install: xlrd
"""


from pandas import read_excel


# import the data
input_file = r'.\inputs\PD 2020 Wk 6 Input.xlsx'
df_rates = read_excel(input_file, sheet_name='GBP to USD conversion rate')
df_sales = read_excel(input_file, sheet_name='Sales')


# parse the rate and calculate the year/week
df_rates['Rate'] =    \
    df_rates['British Pound to US Dollar'].str.extract('\= ([\d\.]+)', expand=False).astype(float)
df_rates['Week'] = [int(d.strftime('%U')) + 1 for d in df_rates['Date']]
df_rates['Year'] = [d.year for d in df_rates['Date']]


# find the min and max rate for each week
df_rates_sum = df_rates.groupby(['Year','Week'], as_index=False).agg( 
                 { 'Rate' : [('Worst','min'),
                             ('Best', 'max')] }
               )
df_rates_sum.columns = ['_'.join(t) if t[1] else t[0] for t in df_rates_sum.columns.values] 


# join rates to sales
df_all = df_sales.merge(df_rates_sum, on=['Year','Week'])


# calculate the UK/US sales and best/worst conversions (rounded to pennies)
df_all['Week'] = 'wk ' + df_all['Week'].astype(str) + ' ' + df_all['Year'].astype(str)
df_all['UK Sales Value (GBP)'] =    \
    round(df_all['Sales Value'] * (1 - df_all['US Stock sold (%)']/100), 2)

df_all['US Sales Value (GBP)'] = df_all['Sales Value'] - df_all['UK Sales Value (GBP)']

df_all['US Sales (USD) Best Case'] =    \
    round(df_all['US Sales Value (GBP)'] * df_all['Rate_Best'], 2)

df_all['US Sales (USD) Worst Case'] =    \
    round(df_all['US Sales Value (GBP)'] * df_all['Rate_Worst'], 2)

df_all['US Sales Potential Variance'] = df_all['US Sales (USD) Best Case']    \
                                        - df_all['US Sales (USD) Worst Case']


# clean up columns
df_all.drop(columns=['Year','Sales Value', 'US Sales Value (GBP)', 'US Stock sold (%)',
                     'Rate_Worst', 'Rate_Best'], inplace=True)


# output the file, reordering the columns to match the example output
df_all.to_csv(path_or_buf=r'.\outputs\output-2020-06.csv', index=False)