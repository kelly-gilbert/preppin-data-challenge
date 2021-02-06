# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2021-04
https://preppindata.blogspot.com/2021/01/2021-week-4.html
 
Pivoting, aggregation, and joins

- Input the file 
- Union the Stores data together
- Remove any unnecessary data fields your Input step might create and rename the 'Table Names' 
    as 'Store' 
- Pivot the product columns
- Split the 'Customer Type - Product' field to create:
   Customer Type
    Product
- Also rename the Values column resulting from you pivot as 'Products Sold'
- Turn the date into a 'Quarter' number
- Sum up the products sold by Store and Quarter
- Add the Targets data 
- Join the Targets data with the aggregated Stores data
    Note: this should give you 20 rows of data
- Remove any duplicate fields formed by the Join
- Calculate the Variance between each Store's Quarterly actual sales and the target. Call this field
    'Variance to Target'
- Rank the Store's based on the Variance to Target in each quarter
    The greater the variance the better the rank
- Output the data

Author: Kelly Gilbert
Created: 2021-02-06
Requirements: 
  - input dataset (PD 2021 Wk 4 Input.xlsx)
  - output dataset (for results check):
    - PD 2021 Wk 4 Output.csv
  
"""


from pandas import concat, ExcelFile, melt, merge, read_csv


# import the data from all sheets and create the Store column
xl = ExcelFile(r'.\inputs\PD 2021 Wk 4 Input.xlsx')

dfTargets = xl.parse('Targets')

dfIn = None
for sheet in [s for s in xl.sheet_names if s != 'Targets']:
    dfNew = xl.parse(sheet)
    dfNew['Store'] = sheet
    dfIn = concat([dfIn, dfNew])

# pivot the columns and rename the new value Products Sold
df = melt(dfIn, id_vars=['Date','Store'], var_name='Customer-Product', value_name='Products Sold')

# split the customer type and product
df[['Customer Type','Product']] = df['Customer-Product'].str.split(pat=' - ', expand=True)

# convert date to quarter
df['Quarter'] = df['Date'].dt.quarter

# sum by store and quarter
dfSum = df.groupby(['Store', 'Quarter'])['Products Sold'].sum().reset_index()

# join the targets to the sales data
dfFinal = dfSum.merge(dfTargets, how='left', on=['Quarter', 'Store'])

# calculate the Variance between each Store's Quarterly actual sales and the target
dfFinal['Variance to Target'] = dfFinal['Products Sold'] - dfFinal['Target']

# rank the Store's based on the Variance to Target in each quarter
dfFinal['Rank'] = dfFinal.groupby(['Quarter'])['Variance to Target'].rank(ascending=False)

# output to csv
dfFinal.to_csv(r'.\outputs\output-2021-04.csv', index=False,
               columns=['Quarter', 'Rank', 'Store', 'Products Sold', 'Target', 'Variance to Target'])


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 4 Output.csv']
my_files = ['output-2021-04.csv']
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