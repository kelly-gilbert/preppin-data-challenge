# -*- coding: utf-8 -*-
"""
Simple examples for profiling Preppin' Data week 2021-51
"""


from line_profiler import LineProfiler
from pandas import read_csv 


def use_factorize():
    # read in the file
    df = read_csv(r'.\inputs\2021W51 Input.csv', parse_dates=['Order Date'], dayfirst=True)
             
    # add customer ID using factorize
    df.sort_values(by=['Order Date', 'Customer'], inplace=True)
    df['CustomerID'] = df['Customer'].factorize()[0] + 1
              
    
    # create the Customer dimension table
    df_cust = df.groupby(['CustomerID', 'Customer'], as_index=False)\
                .agg(First_Order=('Order Date', 'min'))
                
    return df_cust.head()


def use_groupby_and_merge():
    # read in the file
    df = read_csv(r'.\inputs\2021W51 Input.csv', parse_dates=['Order Date'], dayfirst=True)
                       
    
    # create the Customer dimension table
    df_cust = df.groupby(['Customer'], as_index=False)\
                .agg(First_Order=('Order Date', 'min'))\
                .sort_values(by=['First_Order', 'Customer'])\
                .assign(CustomerID=range(1, df['Customer'].nunique()+1))
                
    # add the customer ID to the main table
    df = df.merge(df_cust[['CustomerID', 'Customer']], on='Customer')
                
    return df_cust.head()


# line profiling
%load_ext line_profiler

%lprun -f use_factorize use_factorize()
%lprun -f use_groupby_and_merge use_groupby_and_merge()
