# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 08 - Taking Stock (polars)
https://preppindata.blogspot.com/2023/02/2023-week-8-taking-stock.html

- Input each of the 12 monthly files
- Create a 'file date' using the month found in the file name
  - The Null value should be replaced as 1
- Clean the Market Cap value to ensure it is the true value as 'Market Capitalisation'
  - Remove any rows with 'n/a'
- Categorise the Purchase Price into groupings
  - 0 to 24,999.99 as 'Low'
  - 25,000 to 49,999.99 as 'Medium'
  - 50,000 to 74,999.99 as 'High'
  - 75,000 to 100,000 as 'Very High'
  [KLG note: solution output has Small, Medium, Large, Very Large]
- Categorise the Market Cap into groupings
  - Below $100M as 'Small'
  - Between $100M and below $1B as 'Medium'
  - Between $1B and below $100B as 'Large' 
  - $100B and above as 'Huge'
- Rank the highest 5 purchases per combination of: file date, Purchase Price Categorisation and Market Capitalisation Categorisation.
- Output only records with a rank of 1 to 5

Author: Kelly Gilbert
Created: 2023-06-22
Requirements:
  - input dataset:
      - MOCK_DATA...csv files (12 files)
  - output dataset (for results check only):
      - PD 2023 Wk 8 Output.csv
"""


import polars as pl
import re
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def string_to_number(col_name):
    """
    convert a price in $1.234M to a float (1234000)
    """
    
    return ( pl.col(col_name).str.replace_all('[\$MBK]', '').cast(pl.Float64)
                 * pl.when(pl.col(col_name).str.ends_with('K'))
                     .then(pl.lit(1000))
                     .when(pl.col(col_name).str.ends_with('M'))
                     .then(pl.lit(1_000_000))
                     .when(pl.col(col_name).str.ends_with('B'))
                     .then(pl.lit(1_000_000_000))
                     .otherwise(pl.lit(1))
           )


def market_cap_category():
    """
    return the category for market capitalization
    """

    return ( pl.when(pl.col('Market Capitalisation') < 100_000_000)
               .then('Small')
               .when(pl.col('Market Capitalisation') < 1_000_000_000)
               .then('Medium')
               .when(pl.col('Market Capitalisation') < 100_000_000_000)
               .then('Large')
               .otherwise('Huge') )


def purchase_price_category():
    """
    return the category for purchase price
    """

    return ( pl.when(pl.col('Purchase Price') < 25_000)
               .then('Small')
               .when(pl.col('Purchase Price') < 50_000)
               .then('Medium')
               .when(pl.col('Purchase Price') < 75_000)
               .then('Large')
               .otherwise('Very Large') )


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input files and remove null Market Caps
df = ( pl.concat( 
           [pl.read_csv(f)
              .with_columns(pl.lit(re.match('.*MOCK_DATA-?(\d*)\.csv', f).group(1))
                              .alias('month_nbr'))
            for f in glob(r'.\inputs\MOCK_DATA*.csv')]
       )
    
       # remove n/as
       .filter(pl.col('Market Cap') != 'n/a')
       
       # remove trailing whitespace
       .with_columns(
           pl.col(pl.Utf8).str.strip()
       )
       
       .with_columns(           
           # make the file date
           (pl.lit('01/') 
               + pl.when(pl.col('month_nbr')=='')
                   .then(pl.lit('1'))
                   .otherwise(pl.col('month_nbr'))
                   .str.zfill(2)
               + pl.lit('/2023')).alias('File Date'),
           
           # convert market cap and purchase price to numbers
           string_to_number('Market Cap').alias('Market Capitalisation'),
           string_to_number('Purchase Price')       
       ) 

       # categorize market cap and purchase price
       .with_columns(
           market_cap_category().alias('Market Capitalisation Categorisation'),
           purchase_price_category().alias('Purchase Price Categorisation')
       )   
       
       # rank the purchase price
       .with_columns(
           pl.col('Purchase Price')
             .rank(descending=True)
             .over(['Market Capitalisation Categorisation', 
                    'Purchase Price Categorisation', 
                    'File Date'])
             .cast(pl.Int16)
             .alias('Rank')
       )
       
       # keep top 5
       .filter(pl.col('Rank') <= 5)
    )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Market Capitalisation Categorisation', 'Purchase Price Categorisation', 'File Date', 
            'Ticker', 'Sector', 'Market', 'Stock Name', 'Market Capitalisation', 'Purchase Price', 
            'Rank']

( df.select(out_cols)
    .write_csv(r'.\outputs\output-2023-08.csv', float_precision=2) )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2023 Wk 8 Output.csv']
my_files = [r'.\outputs\output-2023-08.csv']
unique_cols = [['File Date', 
                'Purchase Price Categorisation', 
                'Market Capitalisation Categorisation', 
                'Rank']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)


# ---------------------------------------------------------------------------------------------------
# timing
# ---------------------------------------------------------------------------------------------------

# pandas solution
# 123 ms ± 15 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


# polars dataframe
# 28.7 ms ± 1.36 ms per loop (mean ± std. dev. of 7 runs, 10 loops each)


# polars lazyframe
# 20.2 ms ± 103 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
