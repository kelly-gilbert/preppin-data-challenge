# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-08
https://preppindata.blogspot.com/2020/01/2020-week-8.html
 
Cleaning and joining spreadsheet data

- Input Data
- Pull all the Week worksheets together
- Form weekly sales volume and value figures per product
- Prepare the data in the Profit table for comparison against the actual volumes 
  and values
- Join the tables but only bring back those that have exceeded their Profit Min 
  points for both Value and Volume
- Prepare the Budget Volumes and Values for comparison against the actual volumes
  and values
- Join the tables but only return those that haven't reached the budget expected
  for either Value or Volume
- Prepare the outputs
- Output Data

Author: Kelly Gilbert
Created: 2020-02-15
Requirements: input datasets
  - PD 2020 Wk 7 Current Employees Input.csv
  - PD 2020 Wk 7 Leavers Input.csv
  - PD 2020 Wk 7 Reporting Date Input.csv
"""


from pandas import ExcelFile, read_excel, concat


# import and prep the plan data, starting on row 2
#    remove blank columns
#    trim column names
#    clean type
in_file = ExcelFile(r'.\inputs\PD 2020 Wk 8 Input Not Random.xlsx')
df_profit = in_file.parse(sheet_name='Budget', skiprows=2)
df_profit = df_profit[[c for c in df_profit.columns if 'Unnamed' not in c]]
df_profit.columns = df_profit.columns.str.strip()
df_profit['Type'] = df_profit['Type'].str.lower()


# find the bottom of the profit data and the top of the budget data
last_index = df_profit[df_profit['Week'].isna()].index.min() - 1
budget_start_row = df_profit.loc[df_profit['Week'] == 'Type'].index[0]

df_profit = df_profit[df_profit.index < last_index]


# import and prep the budget data
#    remove blank columns
#    clean type
#    transpose weeks into rows
#    parse week range
#    pivot Measures into cols
df_budget = read_excel(in_file, sheet_name = 'Budget', skiprows=2 + budget_start_row + 1, astype=object)
df_budget = df_budget[[c for c in df_budget.columns if 'Unnamed' not in str(c)]]
df_budget['Type'] = df_budget['Type'].str.lower().str.replace('[^a-z]', '')

df_budget = df_budget.melt(id_vars=['Type', 'Measure'], var_name = 'week_range', 
                           value_name = 'budget')
df_budget['begin_week'] = [int(str(d)[8:10]) for d in df_budget['week_range']]
df_budget['end_week'] = [int(str(d)[5:7]) for d in df_budget['week_range']]
df_budget.drop(columns=['week_range'], inplace=True)

new_index = ['Type', 'begin_week', 'end_week', 'Measure']
df_budget = df_budget.set_index(new_index).unstack('Measure').reset_index()
df_budget.columns = [b if b else a for a, b in df_budget.columns]


# import and prep the sales data
#    read in the 'Week ...' sheets
#    clean the column names
#    sum the volume and value by type
#    add the week number as a column
#    clean the type name
df_sales = None
for s in [s for s in in_file.sheet_names if 'Week' in s]:
    in_sales = read_excel(in_file, sheet_name = s)
    in_sales.columns = in_sales.columns.str.replace('Sales ', '')
    in_sales = in_sales.groupby('Type', as_index=False).agg( 
                                 { 'Volume' : 'sum' , 
                                   'Value': 'sum' }
                                )
    in_sales['week_nbr'] = s.replace('Week ', '')    
    df_sales = concat([df_sales, in_sales])

df_sales['Type'] = df_sales['Type'].str.lower()



# Join the tables but only bring back those that have exceeded their Profit Min 
#  points for both Value and Volume
# Prepare the Budget Volumes and Values for comparison against the actual volumes
#  and values
# Join the tables but only return those that haven't reached the budget expected
#  for either Value or Volume
# Prepare the outputs

