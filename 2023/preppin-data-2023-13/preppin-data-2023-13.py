# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 13 - Rolling stock price trends
https://preppindata.blogspot.com/2023/03/2023-week-13-rolling-stock-price-trends.html

- Input all the months of data available
- Create a Trade Order field showing the order each trade has happened in for each Sector from the File Name and ID as the order of each trade within each monthly file
- Remove all data fields except:
  - Trade Order
  - Sector
  - Purchase Price
- Create a Parameter to allow the user to select the rolling number of trades to be incorporated into the moving average. 
  - I've set a default of 3 trades in my moving average/
- Create a data set that records the previous 2 trades (where applicable) as well as that Trade Order record.
- Workout the Rolling Average Purchase Price for each Trade Order in each Sector
- Filter the data for the last 100 trades for each Sector
- Create the Previous Trades field to show the oldest trade (1) through to the latest trade (100).
- Output the Data

Author: Kelly Gilbert
Created: 2023-07-05
Requirements:
  - input dataset:
      - MOCK DATA...csv files (multiple files)
  - output dataset (for results check only):
      - 3 Trade Rolling Avg. Purchase Price.csv
"""


from glob import glob
import math
import pandas as pd
import re
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = ( pd.concat([pd.read_csv(f)
                    .assign(month=re.search(r'.*MOCK_DATA-?(\d+)?\.csv', f).group(1))
                    .assign(month=lambda df_x: df_x['month'].fillna(1).astype(int))
                  for f in glob(r'.\inputs\MOCK_DATA*')],
                 ignore_index=True)
         .sort_values(['Sector', 'month', 'id']) )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# add the trade order
id_pow = math.ceil(math.log10(df['id'].max()))
df['Trade Order'] = ( df.assign(rank_val = lambda df_x: df_x['month'] * (10**(id_pow+1)) + df_x['id'])
                        .groupby('Sector')
                        ['rank_val'].rank(method='first')
                        .astype(int) )

# convert price to numeric
df['Purchase Price'] = df['Purchase Price'].str.replace('$', '', regex=False).astype(float)


# get user input and output the file
while (trades_in := input('Enter the number of trades for the rolling avg (or Enter to exit):')) != '':
    err_response = 'Please enter a positive integer (or Enter to exit).'
    try:
        trades = int(trades_in)
        if trades <= 0:
            print(err_response)
            continue
            
    except ValueError:
        print(err_response)
        
    else:
        # calculate the rolling average
        df['Rolling Avg. Purchase Price'] = ( df.groupby('Sector', dropna=False)
                                                  ['Purchase Price']
                                                  .transform(lambda g: g.rolling(trades)
                                                                        .mean()
                                                                        .round(2)) )
        # keep last 100 records
        df_out = ( df[['Trade Order', 'Sector', 'Rolling Avg. Purchase Price']]
                     .groupby('Sector', as_index=False, dropna=False)
                     .tail(100)
                     .assign(Previous_Trades = lambda df_x: df_x.groupby('Sector')
                                                                ['Trade Order']
                                                                .rank(method='first')
                                                                .astype(int))
                     .rename(columns = lambda c: c.replace('_', ' '))
                 )
        
        filepath = fr'.\outputs\{trades} Trade Rolling Avg Purchase Price.csv'
        df_out.to_csv(filepath, index=False)
        print(f'--- The file was output to {filepath}')
        

#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\3 Trade Rolling Avg. Purchase Price.csv']
my_files = [r'.\outputs\3 Trade Rolling Avg Purchase Price.csv']
unique_cols = [['Sector', 'Trade Order']]
col_order_matters = False
round_dec = 4

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)


#---------------------------------------------------------------------------------------------------
# timing options for adding the rank
#---------------------------------------------------------------------------------------------------

# make the data larger for timing (2.4M records)
df = pd.concat([df.assign(Sector = 'Sector' + str(r)) for r in range(0,200)], ignore_index=True)


# option 1 - create a composite value to rank on -- FASTEST
# orig 12K = 2.8 ms ± 196 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
#     2.4M = 515 ms ± 22.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit 
df['Trade Order'] = ( df.assign(rank_val = lambda df_x: df_x['month']*10_000 + df_x['id'])
                        .groupby('Sector')
                        ['rank_val'].rank() )


# option 1b - create a composite value to rank on (dynamic)
# orig 12K = 2.92 ms ± 142 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
#     2.4M = 532 ms ± 21.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit 
id_pow = math.ceil(math.log10(df['id'].max()))

df['Trade Order'] = ( df.assign(rank_val = lambda df_x: df_x['month'] * (10**(id_pow+1)) 
                                                        + df_x['id'])
                        .groupby('Sector')
                        ['rank_val'].rank() )


# option 2 - cumsum
# orig 12K = 5.58 ms ± 190 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
#     2.4M = 989 ms ± 57.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit 
df['Trade Order'] = ( df.assign(n = 1)
                        .sort_values(['Sector', 'month', 'id'], ascending=True) 
                        .groupby('Sector')
                        ['n'].cumsum() )


# option 3 - rank on tuples -- SLOWEST
# orig 12K = 71.4 ms ± 1.83 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)
#     2.4M = 28.7 s ± 13.5 s per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit
df['Trade Order'] = ( df.assign(t = df[['month', 'id']].apply(tuple, axis=1))
                        .groupby('Sector')
                        ['t'].rank() )
                     

# option 3 - rank on ngroup -- similar to cumsum
# orig 12K = 5.89 ms ± 574 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
#     2.4M = 755 ms ± 25.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit 
df['Trade Order'] = ( df.assign(order = df.groupby(['Sector', 'month', 'id'], 
                                                   sort=True)
                                          .ngroup())
                        .groupby('Sector')['order'].rank() )



#---------------------------------------------------------------------------------------------------
# timing options for finding the rolling average
#---------------------------------------------------------------------------------------------------

# option 1 - calculate rolling avg on full dataset, then trim -- FASTER
# orig 12K = 4.73 ms ± 467 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
#     2.4M = 534 ms ± 43 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit 
df['Rolling Avg. Purchase Price'] = df.groupby('Sector', dropna=False)['Purchase Price'].transform(lambda g: g.rolling(3).mean())
df_out = ( df[['Trade Order', 'Sector', 'Purchase Price']]
             .groupby('Sector', as_index=False, dropna=False)
             .tail(100) )


# opton 2 - trim to just enough history, then calc rolling avg, then final trim
# orig 12K = 5.74 ms ± 162 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
#     2.4M = 655 ms ± 10.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit 
df_out = ( df[['Trade Order', 'Sector', 'Purchase Price']]
             .groupby('Sector', as_index=False, dropna=False)
             .tail(100 + 2) )

df_out['Rolling Avg. Purchase Price'] = df.groupby('Sector', dropna=False)['Purchase Price'].transform(lambda g: g.rolling(3).mean())
df_out = ( df
             .groupby('Sector', as_index=False, dropna=False)
             .tail(100) )