# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 51 - Departmental December - IT
https://preppindata.blogspot.com/2021/12/2021-week-51-departmental-december-it.html

- Input the Data
- Split out the store name from the OrderID
- Turn the Return State field into a binary Returned field
- Create a Sales field
- Create 3 dimension tables for Store, Customer and Product
- When assigning IDs, these should be created using the dimension and minimum 
  order date fields so that the IDs do not change when later orders are placed
- For the Customer dimension table, we want to include additional fields 
  detailing their total number of orders and the % of products they have returned
- Replace the dimensions with their IDs in the original dataset to create the 
  fact table
- Output the fact and dimension tables

Author: Kelly Gilbert
Created: 2021-12-22
Requirements:
  - input dataset:
      - 2021W51 Input.csv
  - output datasets (for results check only):
      - Customer Dimension Table.csv
      - Order Fact Table.csv
      - Product Dimension Table.csv
      - Store Dimension Table.csv
"""


from numpy import where
from pandas import read_csv


def print_errors(df_in, message):
    if len(df_in) > 0:
        print('-' * (len(message) + 4))
        print(f'{message}\n')
        print(df_in)
        

#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\inputs\2021W51 Input.csv', parse_dates=['Order Date'], dayfirst=True)\
         .rename(columns={'OrderID' : 'OrderID_in'})


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split out the store name from the OrderID
df[['Store', 'OrderID']] = df['OrderID_in'].str.extract('(\w+)\-(\d+)')

print_errors(df[(df['Store'].isna()) | (df['OrderID'].isna())]['OrderID_in'], 
             'The following OrderIDs could not be parsed:')

    
# turn the Return State field into a binary Returned field
df['Returned'] = where(df['Return State'].notna(), 1, 0)


# create a Sales field
df['Sales'] = df['Unit Price'].str.replace('[^\d\.\-]', '', regex=True).astype(float) * df['Quantity']

print_errors(df[df['Sales'].isna()][['Unit Price', 'Quantity']], 'Sales amount could not be calculated:')


# create the Store dimension table
df_store = df.groupby('Store').agg(First_Order=('Order Date', 'min')).reset_index()\
               .sort_values(by=['First_Order', 'Store']).reset_index(drop=True).reset_index()\
               .rename(columns={'First_Order' : 'First Order', 'index' : 'StoreID'})
df_store['StoreID'] += 1


# create the Customer dimension table



- Create 3 dimension tables for Store, Customer and Product
- When assigning IDs, these should be created using the dimension and minimum 
  order date fields so that the IDs do not change when later orders are placed
- For the Customer dimension table, we want to include additional fields 
  detailing their total number of orders and the % of products they have returned
- Replace the dimensions with their IDs in the original dataset to create the 
  fact table
- Output the fact and dimension tables



df.info()




#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2021-51.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['']
my_files = ['output-2021-51.csv']
col_order_matters = True

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_file)
    df_mine = read_csv('.\\outputs\\' + my_files[i])

    # are the fields the same and in the same order?
    solution_cols = list(df_solution.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_solution.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        # round float values
        s = df_solution.dtypes.astype(str)
        for c in s[s.str.contains('float')].index:
            df_solution[c] = df_solution[c].round(8)
            df_mine[c] = df_mine[c].round(8)

        # join the dataframes on all columns except the in flags
        df_solution_compare = df_solution.merge(df_mine, how='outer',
                                                on=list(df_solution.columns),
                                                suffixes=['_solution', '_mine'], indicator=True)

        if len(df_solution_compare[df_solution_compare['_merge'] != 'both']) > 0:
            print('*** Values do not match ***\n')
            print('In solution, not in mine:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'left_only']) 
            print('\n\n')
            print('In mine, not in solution:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'right_only']) 
            
        else:
            print('Values match')

    print('\n')
