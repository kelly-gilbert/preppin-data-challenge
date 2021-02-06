# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2021-03
https://preppindata.blogspot.com/2021/01/2021-week-3.html
 
Pivoting and aggregation

- Input the data source by pulling together all the tables
- Pivot 'New' columns and 'Existing' columns
- Split the former column headers to form:
    Customer Type
    Product
- Rename the measure created by the Pivot as 'Products Sold'
- Create a Store column from the data
- Remove any unnecessary data fields
- Turn Date into Quarter
- Aggregate to form two separate outputs of the number of products sold by:
    Product, Quarter
    Store, Customer Type, Product
- Output each data set as a csv file

Author: Kelly Gilbert
Created: 2021-02-06
Requirements: 
  - input dataset (PD 2021 Wk 3 Input.xlsx)
  - output datasets (for results check):
    - Product Quarter Output
    - Store Customer Product Output
  
"""


from pandas import concat, ExcelFile, melt, read_csv


# import the data from all sheets and create the Store column
xl = ExcelFile(r'.\inputs\PD 2021 Wk 3 Input.xlsx')

dfIn = None
for sheet in xl.sheet_names:
    dfNew = xl.parse(sheet)
    dfNew['Store'] = sheet
    dfIn = concat([dfIn, dfNew])


# pivot the columns and rename the new value Products Sold
df = melt(dfIn, id_vars=['Date','Store'], var_name='Customer-Product', value_name='Products Sold')

# split the customer type and product
df[['Customer Type','Product']] = df['Customer-Product'].str.split(pat=' - ', expand=True)

# convert date to quarter
df['Quarter'] = df['Date'].dt.quarter

# aggregation #1: products sold by product, quarter
groupFields = ['Product', 'Quarter']
agg1 = df.groupby(groupFields)['Products Sold'].sum().reset_index()

# aggregation #2: products sold by store, customer type, product
groupFields = ['Store', 'Customer Type', 'Product']
agg2 = df.groupby(groupFields)['Products Sold'].sum().reset_index()

# output to csv
agg1.to_csv(r'.\outputs\output-2021-03-product-quarter.csv', index=False)
agg2.to_csv(r'.\outputs\output-2021-03-store-customertype-product.csv', index=False)



#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solution_files = ['Product Quarter Output.csv', 'Store Customer Product Output.csv']
my_files = ['output-2021-03-product-quarter.csv', 'output-2021-03-store-customertype-product.csv']
col_order_matters = True

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