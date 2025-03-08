# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 50 - Life Expectancy (polars)
https://preppindata.blogspot.com/2024/12/2024-week-50-life-expectancy.html

- Input the data
- Reshape the data so there is a field for the Country Life Expectancy for each Year, as well as a 
  Continent Avg Life Expectancy field for each Year
- Filter the data to include only years from 1950 to 2020
- Determine the percentage of years (between 1950 and 2020) when a country’s life expectancy was 
  higher than its continent’s average
- Compute the percentage change in life expectancy for each country between 1950 and 2020
- Show the top three countries in each continent with the highest percentage increase in life expectancy
- Round the results to the nearest one decimal place.
- Output the Data

Author: Kelly Gilbert
Created: 2024-03-07
Requirements:
  - input dataset:
      - Life expectancy.csv
      - List of Countries-Continents.csv
  - output dataset (for results check only):
      - 2024W50.csv
"""


import numpy as np
import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_exp = ( 
    pl.scan_csv(r'.\inputs\Life expectancy.csv')
        .rename({'Period life expectancy at birth - Sex: all - Age: 0' : 'life_expectancy'})
        .filter(pl.col('Year').is_between(1950, 2020))
)
df_countries = pl.scan_csv(r'.\inputs\List of Countries-Continents.csv')

countries_dict = dict(zip(df_countries['Country'], df_countries['Continent']))


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# prep and reshape the data
df_out = ( 
    df_exp
        .filter(pl.col('Code').is_not_null())

        # find the continent for each country row
        .join( 
            df_countries,
            left_on='Entity',
            right_on='Country',
            how='left'
        )

        # add the continent life expectancy
        .join(
            df_exp
                .filter(pl.col('Code').is_null())
                .select([pl.col('Entity'), pl.col('Year'), pl.col('life_expectancy')]),
            left_on=['Continent', 'Year'],
            right_on=['Entity', 'Year'],
            how='left',
            suffix='_continent'
        )
 
        # calculate % years higher than continent and % change
        .with_columns( 
            (pl.col('life_expectancy') >= pl.col('life_expectancy_continent'))
                .alias('higher_than_continent'),
            pl.when(pl.col('Year') == pl.col('Year').min().over('Entity'))
              .then(pl.col('life_expectancy'))
              .alias('life_expectancy_first'),
            pl.when(pl.col('Year') == pl.col('Year').max().over('Entity'))
              .then(pl.col('life_expectancy'))
              .alias('life_expectancy_last')
        )
        .group_by([pl.col('Continent'), pl.col('Entity')])
        .agg( 
            pl.col('higher_than_continent')
                .sum()
                .alias('years_higher_than_continent'),
            pl.col('Year')
                .count()
                .alias('years'),
            pl.col('life_expectancy_first')
                .max() 
                .alias('life_expectancy_first'),
            pl.col('life_expectancy_last')
                .max() 
                .alias('life_expectancy_last')
        )
        .with_columns( 
            (pl.col('years_higher_than_continent') / pl.col('years') * 100)
                .round(1)
                .alias('% Years Above Continent Avg'),
            ((pl.col('life_expectancy_last') / pl.col('life_expectancy_first') - 1) * 100)
                .round(1)
                .alias('% Change')
        )
        .with_columns( 
            pl.col('% Change')
                .rank(method='dense', descending=True)
                .over('Continent')
                .alias('Rank')
        )

        # prep final output
        .filter(pl.col('Rank') <= 3)
        .select([
            pl.col('Continent'), 
            pl.col('Rank'), 
            pl.col('Entity').alias('Country'), 
            pl.col('% Years Above Continent Avg'), 
            pl.col('% Change')
        ])
)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.collect().write_csv(r'.\outputs\output-2024-50.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2024W50.csv']
my_files = [r'.\outputs\output-2024-50.csv']
unique_cols = [['Country']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
