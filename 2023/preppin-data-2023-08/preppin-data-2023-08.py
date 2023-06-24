# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 08 - Taking Stock
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


from glob import glob
from numpy import where
import pandas as pd
import re
from output_check import output_check    # custom function for checking my output vs. the solution


# ---------------------------------------------------------------------------------------------------
# input the data
# ---------------------------------------------------------------------------------------------------

# input files and remove null Market Caps
df = (pd.concat([pd.read_csv(f)
                    .assign(month_nbr=re.match('.*MOCK_DATA-?(\d*)\.csv', f).group(1))
                for f in glob(r'.\inputs\MOCK_DATA*.csv')],
               ignore_index=True)
         .query("`Market Cap` == `Market Cap`"))


# ---------------------------------------------------------------------------------------------------
# process the data
# ---------------------------------------------------------------------------------------------------

# create the file date
df['File Date'] = pd.to_datetime(df['month_nbr'].fillna(1).astype(str) + '/1/2023')


# remove leading/trailing whitespace
str_cols = [c for c in df.columns if df[c].dtype=='object']
df[str_cols] = df[str_cols].apply(lambda c: c.str.strip())


# clean and categories the market cap value
df['Market Capitalisation']= (df['Market Cap'].str.replace('[\$BM]', '', regex=True).astype(float)
                                * where(df['Market Cap'].str[-1:] == 'M',
                                        1_000_000,
                                  where(df['Market Cap'].str[-1:] == 'B',
                                        1_000_000_000,
                                        1)))


df['Market Capitalisation Categorisation'] = \
    pd.cut(df['Market Capitalisation'],
           right=False,
           include_lowest=True,
           bins=[0, 100_000_000, 1_000_000_000, 100_000_000_000, 999_999_999_999_999],
           labels=['Small', 'Medium', 'Large', 'Huge'])


# clean and categorize the purchase price
df['Purchase Price']= (df['Purchase Price']
                           .str.replace('$', '', regex=True)
                           .astype(float))


df['Purchase Price Categorisation'] = \
    pd.cut(df['Purchase Price'],
           right=False,
           include_lowest=True,
           bins=[0, 25_000, 50_000, 75_000, 999_999_999],
           labels=['Small', 'Medium', 'Large', 'Very Large'])


# rank purchases
df['Rank'] = ( df.groupby(['File Date',
                           'Purchase Price Categorisation',
                           'Market Capitalisation Categorisation'])
                 ['Purchase Price'].rank(ascending=False).astype(int) )


# ---------------------------------------------------------------------------------------------------
# output the file
# ---------------------------------------------------------------------------------------------------

out_cols= ['Market Capitalisation Categorisation', 'Purchase Price Categorisation', 'File Date',
            'Ticker', 'Sector', 'Market', 'Stock Name', 'Market Capitalisation', 'Purchase Price',
            'Rank']

df[df['Rank'] <= 5].to_csv(r'.\outputs\output-2023-08.csv',
                           index=False,
                           columns=out_cols,
                           float_format='%.2f',
                           date_format='%d/%m/%Y')


# ---------------------------------------------------------------------------------------------------
# check results
# ---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2023 Wk 8 Output.csv']
my_files = [r'.\outputs\output-2023-08.csv']
unique_cols= [['File Date',
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