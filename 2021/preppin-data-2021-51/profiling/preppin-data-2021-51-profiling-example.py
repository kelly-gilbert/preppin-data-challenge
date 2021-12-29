# -*- coding: utf-8 -*-
"""
Simple examples for profiling Preppin' Data week 2021-51
"""


from line_profiler import LineProfiler
from os import chdir
from pandas import DataFrame, date_range
import random as rnd
import string


# quick comparison of the solution script using timeit -- run time is similar
# chdir(r'.\profiling')
# %timeit -n 1 -r 1000 %run preppin-data-2021-51-factorize.py
# %timeit -n 1 -r 1000 %run preppin-data-2021-51-group-and-merge.py


# --------------------------------------------------------------------------------------------------
# define functions
# --------------------------------------------------------------------------------------------------

def create_data(recs, card='low'):
    # generate sample data
    rnd.seed(0)
    
    # similar cardinality to the sample dataset (380 choices)
    if card == 'sample':
        return DataFrame({'Customer' : [''.join(rnd.choices('ABCDEFGHIJKLMNOPQRST', k=2))*10 
                                        for n in range(0, recs)],
                          'Order Date' : rnd.choices(date_range('2000-01-01', '2021-12-31'), k=recs)})

    # low cardinality customer (52 possible choices)
    elif card == 'low':
        return DataFrame({'Customer' : [rnd.choice(string.ascii_letters)*20 for n in range(0, recs)],
                          'Order Date' : rnd.choices(date_range('2000-01-01', '2021-12-31'), k=recs)})
                          
    # medium cardinality customer (2,652 possible choices)
    elif card == 'med':
        return DataFrame({'Customer' : [''.join(rnd.choices(string.ascii_letters, k=2))*10 
                                        for n in range(0, recs)],
                          'Order Date' : rnd.choices(date_range('2000-01-01', '2021-12-31'), k=recs)})

    # high cardinality customer (5.74 x 10^16 possible choices)
    else:
        return DataFrame({'Customer' : [''.join(rnd.choices(string.ascii_letters, k=10))*2 
                                        for n in range(0, recs)],
                          'Order Date' : rnd.choices(date_range('2000-01-01', '2021-12-31'), k=recs)})


def use_factorize(df):
    # add customer ID using factorize
    df.sort_values(by=['Order Date', 'Customer'], inplace=True)
    df['CustomerID'] = df['Customer'].factorize()[0] + 1
                  
    # create the Customer dimension table
    df_cust = df.groupby(['CustomerID', 'Customer'], as_index=False)\
                .agg(First_Order=('Order Date', 'min'))


def use_groupby_and_merge(df):
    # create the Customer dimension table
    df_cust = df.groupby(['Customer'], as_index=False)\
                .agg(First_Order=('Order Date', 'min'))\
                .sort_values(by=['First_Order', 'Customer'])\
                .assign(CustomerID=range(1, df['Customer'].nunique()+1))
                
    # add the customer ID to the main table
    df = df.merge(df_cust[['CustomerID', 'Customer']], on='Customer')


def run_factorize():
    df = create_data(1000000, card='high')
    use_factorize(df)
    
def run_groupby_and_merge():
    df = create_data(1000000, card='high')
    use_groupby_and_merge(df)


# --------------------------------------------------------------------------------------------------
# line profiling
# --------------------------------------------------------------------------------------------------

%load_ext line_profiler

%lprun -u 0.001 -f use_factorize run_factorize()
%lprun -u 0.001 -f use_groupby_and_merge run_groupby_and_merge()
