# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 15 - Restaurant Menu & Orders
https://preppindata.blogspot.com/2021/04/2021-week-15-restaurant-menu-orders.html

- Input the data
- Modify the structure of the Menu table so we can have one column for the Type (pizza, pasta,
  house plate), the name of the plate, ID, and Price
- Modify the structure of the Orders table to have each item ID in a different row
- Join both tables
- On Mondays we offer a 50% discount on all items. Recalculate the prices to reflect this
- For Output 1, we want to calculate the total money for each day of the week
- For Output 2, we want to reward the customer who has made the most orders for their loyalty.
  Work out which customer has ordered the most single items.

Author: Kelly Gilbert
Created: 2021-05-11
Requirements:
  - pandas version 0.25.0 or higher (for explode)
  - input dataset:
      - Menu and Orders.xlsx
  - output dataset (for results check):
      - Output 1.csv
      - Output 2.csv
"""

from numpy import where
from pandas import DataFrame, ExcelFile, melt, pivot_table, read_excel

# for results check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Menu and Orders.xlsx') as xl:
    menu = read_excel(xl, 'MENU')
    orders = read_excel(xl, 'Order')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# modify the menu data so we can have one column for the type, name, ID, and price

# melt the columns into rows
menu = menu.reset_index().melt(id_vars=['index'])

# parse the fieldnames and remove nulls
menu[['Type', 'field']] = menu['variable'].str.extract('(.*?)\s?(ID|Price|$).*', expand=True)
menu['field'] = where(menu['field'].str.strip() == '', 'Item', menu['field'])
menu.dropna(subset=['value'], inplace=True)

# pivot fieldnames into columns
menu_f = menu.pivot_table(values='value', index=['index', 'Type'], columns=['field'],
                          aggfunc='first')\
             .reset_index()\
             .drop(columns='index')


# put each item ID from orders into a separate row
orders['Order'] = orders['Order'].astype(str).str.split('-')
orders = orders.explode('Order')
orders['Order'] = orders['Order'].astype(int)

# join the tables
orders_f = orders.merge(menu_f, left_on='Order', right_on='ID', how='inner')

# apply 50% discount on Mondays
orders_f['Weekday'] = orders_f['Order Date'].dt.day_name()
orders_f['Price'] = where(orders_f['Weekday'] == 'Monday', orders_f['Price'] * 0.5,
                          orders_f['Price'])


#---------------------------------------------------------------------------------------------------
# output the files
#---------------------------------------------------------------------------------------------------

# output 1: calculate total spend by day of week
out1 = orders_f.groupby('Weekday')['Price'].sum().reset_index()
out1.to_csv(r'.\outputs\output-2021-15-01.csv', index=False, columns=['Price', 'Weekday'])


# output 2: customer with the most single items (count of unique items)
out2 = orders_f.groupby('Customer Name')['Order'].nunique().reset_index()\
               .sort_values(by='Order', ascending=False).iloc[0:1, :]
out2.rename(columns={'Order':'Count Items'}, inplace=True)

out2.to_csv(r'.\outputs\output-2021-15-02.csv', index=False,
            columns=['Count Items', 'Customer Name'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solutionFiles = ['Output 1.csv', 'Output 2.csv']
myFiles = ['output-2021-15-01.csv', 'output-2021-15-02.csv']
col_order_matters = False

for i in range(len(solutionFiles)):
    print('---------- Checking \'' + solutionFiles[i] + '\' ----------\n')

    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solutionFiles[i])
    dfMine = read_csv('.\\outputs\\' + myFiles[i])

    # are the fields the same and in the same order?
    solutionCols = list(dfSolution.columns)
    myCols = list(dfMine.columns)
    if not col_order_matters:
        solutionCols.sort()
        myCols.sort()

    col_match = False
    if solutionCols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(dfSolution.columns)))
        print('    Columns in mine    : ' + str(list(dfMine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        dfSolution['join'] = 1
        dfMine['join'] = 1
        dfCompare = dfSolution.merge(dfMine, how='outer', on=list(dfSolution.columns)[:-1])
        dfCompare.rename(columns={'join_x':'in_solution', 'join_y':'in_mine'}, inplace=True)

        if dfCompare['in_solution'].count() != len(dfCompare):
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')

    print('\n')
