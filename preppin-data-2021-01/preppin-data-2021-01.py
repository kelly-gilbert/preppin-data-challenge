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
from pandas import DataFrame, read_csv
import seaborn as sns


# connect and load the csv file
chdir('C:\\projects\\preppin-data-challenge\\preppin-data-2021-01')

df = read_csv('.\\inputs\\PD 2021 Wk 1 Input - Bike Sales.csv', 
              parse_dates=['Date'], dayfirst=True)

# split the 'Store-Bike' field into 'Store' and 'Bike'
df[['Store','Bike']] = df['Store - Bike'].str.split(pat=' - ', expand=True)

# clean up the 'Bike' field to leave just three values in the 'Bike' field 
# (Mountain, Gravel, Road)
remap = { 'Graval' : 'Gravel',
          'Gravle' : 'Gravel',
          'Mountaen' : 'Mountain',
          'Rood' : 'Road',
          'Rowd' : 'Road' }
df['Bike'].replace(remap, inplace=True)

# create two different cuts of the date field: 'quarter' and 'day of month'
df['Quarter'] = df['Date'].dt.quarter
df['Day of Month'] = df['Date'].dt.day

# remove the first 10 orders as they are test values
df = df.iloc[10:]

# output the data as a csv
col_order = ['Quarter', 'Store', 'Bike', 'Order ID', 'Customer Age',
             'Bike Value', 'Existing Customer?', 'Day of Month']
df[col_order].to_csv('.\\outputs\\output-2021-01.csv', index=False)


#--------------------------------------------------------------------------------
# bonus
#--------------------------------------------------------------------------------

df = read_csv('.\\outputs\\output-2021-01.csv')

# create a list of all possible combinations
df_qtr = DataFrame({ 'Quarter' : df['Quarter'].unique() }).sort_values(by='Quarter')
df_qtr['join'] = 1
df_day = DataFrame({ 'Day of Month' : range(1,32) }).sort_values(by='Day of Month')
df_day['join'] = 1
df_bike = DataFrame({ 'Bike' : df['Bike'].unique() }).sort_values(by='Bike')
df_bike['join'] = 1

df_all = df_qtr.merge(df_day, how='outer', on='join')
df_all = df_all.merge(df_bike, how='outer', on='join')


# average bike value per order by type, quarter, and day of month
# (not sure how this is useful, but this is the calc used in the solution!)
df_sum = df.groupby(['Bike', 'Quarter', 'Day of Month'])['Bike Value'].mean()
df_sum = df_sum.reset_index()


# add the sum
df_all = df_all.merge(df_sum, how='left', on=['Quarter', 'Day of Month', 'Bike']).fillna(0)
df_all['Cuml Sales'] = df_all.groupby(['Bike','Quarter'])['Bike Value'].cumsum()


# generate charts by quarter
sns.set_style("white")
palette = ['#ccb22b','#9f8f12','#959c9e']

g = sns.FacetGrid(df_all, row="Quarter",
                  aspect=5, height=1.5, sharex=True, sharey=False,
                  legend_out=True, margin_titles=False) 

g.fig.suptitle("Typical Running Monthly Sales in Each Quarter", 
               x=0.3, y=1.05, fontsize='xx-large')

g.map(sns.lineplot, "Day of Month", "Cuml Sales", 'Bike', 
      palette=palette, ci=None, linewidth=2.5).add_legend(loc='upper right')


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
else:
    print('Columns match\n')


# are the values the same?
df_solution['check'] = 1
df_mine['check'] = 1
df_compare = df_solution.merge(df_mine, how='outer', 
                               on=list(df_solution.columns)[:-1])

if df_compare['check_x'].count() != len(df_compare):
    print('*** Values do not match ***')
    print(df_compare[df_compare['check_x'] != df_compare['check_y']])
else:
    print('Values match')
