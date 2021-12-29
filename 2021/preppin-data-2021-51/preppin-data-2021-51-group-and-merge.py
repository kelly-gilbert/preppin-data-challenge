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


# create the Store dimension table
df_store = df.groupby('Store')['Order Date'].min().reset_index()\
             .sort_values(by=['Order Date', 'Store'], key=sort_ignorecase)\
             .rename(columns={'Order Date' : 'First Order'})
df_store['StoreID'] = range(1, len(df_store) + 1)


# create the Customer dimension table
df_cust = df.groupby('Customer').agg(Returned=('Returned', 'sum'),
                                     Order_Lines=('OrderID', 'count'),
                                     Number_of_Orders=('OrderID', 'nunique'),
                                     First_Order=('Order Date', 'min')).reset_index()\
            .sort_values(by=['First_Order', 'Customer'], key=sort_ignorecase)
df_cust.columns = [c.replace('_', ' ') for c in df_cust.columns]
df_cust['Return %'] = (df_cust['Returned'] / df_cust['Order Lines']).round(2)
df_cust['CustomerID'] = range(1, len(df_cust) + 1)


# create the Product dimension table
df_prod = df.groupby(['Category', 'Sub-Category', 'Product Name'])\
            .agg(Unit_Price=('Unit Price', 'mean'),
                 First_Sold=('Order Date', 'min')).reset_index()\
            .sort_values(by=['First_Sold', 'Product Name'], key=sort_ignorecase)
df_prod.columns = [c.replace('_', ' ') for c in df_prod.columns]
df_prod['ProductID'] = range(1, len(df_prod) + 1)


# replace the dimensions with their IDs in the original dataset to create the fact table
df = df.merge(df_store[['StoreID', 'Store']], on='Store', how='left')\
       .merge(df_cust[['CustomerID', 'Customer']], on='Customer', how='left')\
       .merge(df_prod[['ProductID', 'Product Name']], on='Product Name', how='left')
