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
Created: 2023-07-11
Requirements:
  - input dataset:
      - MOCK DATA...csv files (multiple files)
  - output dataset (for results check only):
      - 3 Trade Rolling Avg. Purchase Price.csv
"""


from glob import glob
import polars as pl
import re
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input and prep the data
#---------------------------------------------------------------------------------------------------

df = ( pl.concat( 
           [pl.scan_csv(f)
              .with_columns(pl.lit(re.match('.*MOCK_DATA-?(\d*)\.csv', f).group(1))
                              .alias('month_nbr'))
            for f in glob(r'.\inputs\MOCK_DATA*.csv')]
       )
    
       # fill in month number and convert purchase price to numeric
       .with_columns( 
           pl.when(pl.col('month_nbr')=='')
             .then(pl.lit(1))
             .otherwise(pl.col('month_nbr'))
             .cast(pl.Int8)
             .alias('month_nbr'),
          pl.col('Purchase Price').str.replace('$', '', literal=True)
            .cast(pl.Float64)
       )
       
       # rank within Sector
       .with_columns(
           pl.struct(pl.col(['month_nbr', 'id']))
             .rank().over(pl.col('Sector'))
             .cast(pl.Int16)
             .alias('Trade Order')
       ) 
       
       # remove extra fields
       .select(pl.col(['Trade Order', 'Sector', 'Purchase Price']))
       
     )


#---------------------------------------------------------------------------------------------------
# get user input and output the file
#---------------------------------------------------------------------------------------------------

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
        df_out = ( df.sort(pl.col(['Sector', 'Trade Order']))
                  
                     # calculate rolling average
                     .select( 
                        pl.col(['Trade Order', 'Sector']),
                        pl.col('Purchase Price').rolling_mean(trades).over(pl.col('Sector'))
                          .round(2)
                          .alias('Rolling Avg. Purchase Price')
                     )
                     
                     # keep the last 100
                     .groupby('Sector').tail(100)
                     
                     # add the previous trade number
                     .with_columns( 
                         pl.col('Trade Order').rank().over('Sector')
                           .cast(pl.Int16)
                           .alias('Previous Trades')
                     )
                 )


        # output the file
        filepath = fr'.\outputs\{trades} Trade Rolling Avg Purchase Price.csv'
        df_out.collect().write_csv(filepath)
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
