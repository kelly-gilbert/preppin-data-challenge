# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2021-02
https://preppindata.blogspot.com/2021/01/2021-week-1.html
 
Aggregation

- Input the data
- Clean up the Model field to leave only the letters to represent the Brand of 
  the bike
- Workout the Order Value using Value per Bike and Quantity.
- Aggregate Value per Bike, Order Value and Quantity by Brand and Bike Type 
  to form:
  Quantity Sold
  Order Value
  Average Value Sold per Brand, Type
- Calculate Days to ship by measuring the difference between when an order was 
  placed and when it was shipped as 'Days to Ship'
- Aggregate Order Value, Quantity and Days to Ship by Brand and Store to form:
  Total Quantity Sold
  Total Order Value
  Average Days to Ship
- Round any averaged values to one decimal place to make the values easier to read
- Output both data sets

Author: Kelly Gilbert
Created: 2021-01-14
Requirements: 
  - input dataset (PD 2021 Wk 2 Input - Bike Model Sales.csv)
  - output dataset (for results check, PD 2021 Wk 1 Output.csv)
  
"""


from pandas import read_csv


# input the data
df = read_csv('.\\inputs\\PD 2021 Wk 2 Input - Bike Model Sales.csv', 
              parse_dates=['Order Date', 'Shipping Date'], dayfirst=True)


# clean up the Model field to leave only the letters to represent the 
# Brand of the bike
df['Brand'] = df['Model'].str.replace('[^A-Z]+', '')


# work out the Order Value using Value per Bike and Quantity
df['Order Value'] = df['Value per Bike'] * df['Quantity']


# aggregate Value per Bike, Order Value and Quantity by Brand and Bike Type 
# note, the avg value sold is the straight average and not weighted
df_brand = df.groupby(['Brand', 'Bike Type']).agg({ 'Quantity' : ['sum'],
                                                    'Order Value' : ['sum'],
                                                    'Value per Bike' : ['mean'] })
df_brand.columns = ['Quantity Sold', 'Order Value', 'Avg Bike Value Sold per Brand, Type']
df_brand.reset_index(inplace = True)

df_brand['Avg Bike Value Sold per Brand, Type'] = \
    df_brand['Avg Bike Value Sold per Brand, Type'].round(1)


# calculate Days to ship by measuring the difference between when an order was 
#  placed and when it was shipped as 'Days to Ship'
df['Days to Ship'] = (df['Shipping Date'] - df['Order Date']).dt.days
df[['Order Date', 'Shipping Date', 'Days to Ship']].head()

   
# aggregate Order Value, Quantity and Days to Ship by Brand and Store
df_store = df.groupby(['Brand', 'Store']).agg({ 'Quantity' : ['sum'],
                                                'Order Value' : ['sum'],
                                                'Days to Ship' : ['mean']})
df_store.columns = ['Total Quantity Sold', 'Total Order Value', 'Avg Days to Ship']
df_store.reset_index(inplace = True)

df_store['Avg Days to Ship'] = df_store['Avg Days to Ship'].round(1)


# output both data sets
df_brand.to_csv('.\\outputs\\output-2021-02-brand-type.csv', index = False)
df_store.to_csv('.\\outputs\\output-2021-02-brand-store.csv', index = False)


#--------------------------------------------------------------------------------
# not part of the challenge, just practice making charts
#--------------------------------------------------------------------------------

import seaborn as sns


sns.set_style('white')
sns.set_palette('Set2')

# quantity sold by brand
g = sns.catplot(data=df_brand, x='Brand', y='Quantity Sold', estimator=sum, kind='bar', ci=None,
                aspect=2, height=3)
g.fig.suptitle("Quantity Sold by Brand", y=1.05, fontsize='x-large')


# quantity sold by type
g = sns.catplot(data=df_brand, x='Bike Type', y='Quantity Sold', estimator=sum, kind='bar', ci=None,
                aspect=2, height=3)
g.fig.suptitle("Quantity Sold by Bike Type", y=1.05, fontsize='x-large')


# quantity sold by brand and type
# using the palette from week 1
palette = ['#ccb22b','#9f8f12','#959c9e']
g = sns.catplot(data=df_brand, x='Brand', y='Quantity Sold', estimator=sum, kind='bar', ci=None,
                hue='Bike Type', palette=palette, aspect=2, height=3)
g.fig.suptitle("Quantity Sold by Brand and Bike Type", y=1.05, fontsize='x-large')


# quantity sold by month and type
df['Order Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()
palette = ['#ccb22b','#9f8f12','#959c9e']
g = sns.relplot(data=df, x='Order Month', y='Quantity', estimator=sum, kind='line', ci=None,
                hue='Bike Type', palette=palette, aspect=2, height=3)
g.fig.suptitle("Quantity Sold by Month and Bike Type", y=1.05, fontsize='x-large')


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 2 Brand Type.csv', 'PD 2021 Wk 2 Brand Store.csv']
my_files = ['output-2021-02-brand-type.csv', 'output-2021-02-brand-store.csv']
col_order_matters = False

for i in range(len(solution_files)):
    print('---------- Checking \'' + solution_files[i] + '\' ----------\n')
    
    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_files[i])
    df_mine = read_csv('.\\outputs\\' + my_files[i])
    
    # are the fields the same and in the same order?
    solution_cols = list(df_solution.columns)
    my_cols = list(df_mine.columns)
    if col_order_matters == False:
         solution_cols.sort()
         my_cols.sort()

    col_match = False
    if solution_cols != my_cols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_solution.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
    else:
        print('Columns match\n')
        col_match = True
    
    # are the values the same? (only check if the columns matched)
    if col_match == True:
        df_solution['check'] = 1
        df_mine['check'] = 1
        df_compare = df_solution.merge(df_mine, how='outer', on=list(df_solution.columns)[:-1])
        
        if df_compare['check_x'].count() != len(df_compare):
            print('*** Values do not match ***')
            print(df_compare[df_compare['check_x'] != df_compare['check_x']])
        else:
            print('Values match')
    
    print('\n')