# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 50 - Life Expectancy
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
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_exp = ( 
    pd.read_csv(r'.\inputs\Life expectancy.csv')
        .rename(columns={'Period life expectancy at birth - Sex: all - Age: 0' : 'life_expectancy'})
        .query("(Year >= 1950) & (Year <= 2020)")
)
df_countries = pd.read_csv(r'.\inputs\List of Countries-Continents.csv')

countries_dict = dict(zip(df_countries['Country'], df_countries['Continent']))


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# prep and reshape the data
df_out = ( 
    df_exp
        [df_exp['Code'].notna()]

        # find the continent for each country row
        .assign(
            Continent = lambda df_x: \
                np.where(
                    df_x['Entity'].isin(countries_dict.keys()),
                    df_x['Entity'].replace(countries_dict),
                    None
                )
        )

        # add the continent life expectancy
        .merge(
            df_exp[df_exp['Code'].isna()][['Entity', 'Year', 'life_expectancy']],
            left_on=['Continent', 'Year'],
            right_on=['Entity', 'Year'],
            how='left',
            suffixes=['', '_continent']
        )
 
        # calculate % years higher than continent and % change
        .assign( 
            higher_than_continent = lambda df_x: \
                (df_x['life_expectancy'] >= df_x['life_expectancy_continent']),
            life_expectancy_first = lambda df_x: \
                np.where(
                    df_x['Year'] == df_x.groupby('Entity')['Year'].transform('min'),
                    df_x['life_expectancy'],
                    np.nan
                ),
            life_expectancy_last = lambda df_x: \
                np.where(
                    df_x['Year'] == df_x.groupby('Entity')['Year'].transform('max'),
                    df_x['life_expectancy'],
                    np.nan
                )
        )
        .groupby(['Continent', 'Entity'], as_index=False)
        .agg( 
            years_higher_than_continent = ('higher_than_continent', 'sum'),
            years = ('Year', 'count'),
            life_expectancy_first = ('life_expectancy_first', 'max'),
            life_expectancy_last = ('life_expectancy_last', 'max')
        )
        .assign( 
            **{'% Years Above Continent Avg' : lambda df_x: \
                    (df_x['years_higher_than_continent'] / df_x['years'] * 100).round(1),
               '% Change' : lambda df_x: \
                   ((df_x['life_expectancy_last'] / df_x['life_expectancy_first'] - 1) * 100).round(1)
              }
        )
        .assign( 
            Rank = lambda df_x: df_x.groupby('Continent')['% Change'].rank(method='dense', ascending=False)
        )

        # prep final output
        .query("Rank <= 3")
        [['Continent', 'Rank', 'Entity', '% Years Above Continent Avg', '% Change']]
        .rename(columns={'Entity' : 'Country'})
)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2024-50.csv', index=False)


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
