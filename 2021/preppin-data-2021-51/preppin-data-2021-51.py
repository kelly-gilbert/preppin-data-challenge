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


from pandas import read_csv


def print_errors(df_in, message):
    if len(df_in) > 0:
        print('-' * (len(message) + 4))
        print(f'{message}\n')
        print('-' * (len(message) + 4))
        print(df_in)


def sort_ignorecase(x):
    if x.dtype == 'O':
        return x.str.lower()
    else:
        return x


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\inputs\2021W51 Input.csv', parse_dates=['Order Date'], dayfirst=True)\
         .rename(columns={'OrderID' : 'OrderID_in', 'Unit Price' : 'Unit Price_in'})


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split out the store name from the OrderID
df[['Store', 'OrderID']] = df['OrderID_in'].str.extract('(\D+)-(\d+)', expand=True)

    
# turn the Return State field into a binary Returned field
df['Returned'] = where(df['Return State'].notna(), 1, 0)


# create a Sales field
df['Unit Price'] = df['Unit Price_in'].str.replace('[^\d\.\-]', '', regex=True).astype(float) 
df['Sales'] = df['Unit Price'] * df['Quantity']


# add IDs
for c in ['Store', 'Customer', 'Product Name']:
    df.sort_values(by=['Order Date', c], key=sort_ignorecase, inplace=True)
    df[f"{c.replace(' Name', '')}ID"] = df[c].factorize()[0] + 1


# create the Store dimension table
df_store = df.groupby(['StoreID', 'Store'])['Order Date'].min().reset_index()\
             .rename(columns={'Order Date' : 'First Order'})
             

# create the Customer dimension table
df_cust = df.groupby(['CustomerID', 'Customer'])\
            .agg(Returned=('Returned', 'sum'),
                 Order_Lines=('OrderID', 'count'),
                 Number_of_Orders=('OrderID', 'nunique'),
                 First_Order=('Order Date', 'min')).reset_index()
df_cust.columns = [c.replace('_', ' ') for c in df_cust.columns]
df_cust['Return %'] = (df_cust['Returned'] / df_cust['Order Lines']).round(2)


# create the Product dimension table
df_prod = df.groupby(['ProductID', 'Category', 'Sub-Category', 'Product Name'])\
            .agg(Unit_Price=('Unit Price', 'mean'),
                 First_Sold=('Order Date', 'min')).reset_index()
df_prod.columns = [c.replace('_', ' ') for c in df_prod.columns]


#---------------------------------------------------------------------------------------------------
# output the files
#---------------------------------------------------------------------------------------------------

df_store.to_csv(r'.\outputs\output-2021-51-store.csv', index=False, date_format='%d/%m/%Y',
                columns=['StoreID', 'Store', 'First Order'])
df_cust.to_csv(r'.\outputs\output-2021-51-customer.csv', index=False, date_format='%d/%m/%Y',
               columns=['CustomerID', 'Customer', 'Return %', 'Number of Orders', 'First Order'])
df_prod.to_csv(r'.\outputs\output-2021-51-product.csv', index=False, date_format='%d/%m/%Y',
               columns=['ProductID', 'Category', 'Sub-Category', 'Product Name', 'Unit Price', 
                        'First Sold'])
df.to_csv(r'.\outputs\output-2021-51-order.csv', index=False, date_format='%d/%m/%Y',
          columns=['StoreID', 'CustomerID', 'OrderID', 'Order Date', 'ProductID', 'Returned',
                   'Quantity', 'Sales'])

      
#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Store Dimension Table.csv', 'Customer Dimension Table.csv', 
                  'Product Dimension Table.csv', 'Order Fact Table.csv']
my_files = ['output-2021-51-store.csv', 'output-2021-51-customer.csv',
            'output-2021-51-product.csv', 'output-2021-51-order.csv']
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
