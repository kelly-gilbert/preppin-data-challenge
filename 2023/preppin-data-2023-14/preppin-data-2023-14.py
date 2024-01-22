# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 14 - challenge title goes here
https://preppindata.blogspot.com/ - challenge url goes here

- Input the world trade data, pull in all countries’ files
  - Make sure Prep reads the first line of the file as header
- Update the data role of the Reporter and Partner fields from string to 
  Country/ Region (some countries will not be recognised, but we will keep them in)
- Get the country code for each country from the file path
  - E.g AFG for Afghanistan 
- Keep Import and Export data only
  - Remove “World”, “European Union”, “"Occ.Pal.Terr" and "Other Asia, nes" in the Reporter column 
    as they are not countries
  - Remove “…”, “Special Category” and “World” in the Partner column
- Remove file path
- Make sure all years are in the same column
  - Name it “Year” and change data type to date 
- Change the pivoted value to number (decimal) and pivot them up as column
- Input the Countries geo data
- Remove unnecessary columns
- Get the latitude and longitude from the “geo_point_2d” column 
  - First coordinate as Latitude, second as Longitude
  - Make sure the data type is number(decimal)
- Join the countries geo data to the trade data
  - Make sure no record from the trade data is lost from the join
  - Remove countries name and code fields from the geo data
- After getting the latitude and longitude for the reporting country, we now need to get the same 
  for partner countries as well
  - Get the country code for the partner country and join with geo data again to get the coordinates 
    for the partner countries
  - Add suffix “_Partner” to the latitude and longitude of partners
- Output the data

Author: Kelly Gilbert
Created: 2023-08-06
Requirements:
  - input dataset:
      - countries-codes.csv
      - wits_en_trade_summary_allcountries_allyears (3).zip
  - output dataset (for results check only):
      - World Imports and Exports.csv
"""


import pandas as pd
from zipfile import ZipFile
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

# values to include/exclude from the zipped files
INCL_INDICATOR_TYPE = ['Import', 'Export']
EXCL_REPORTER = [' World', 'European Union', 'Occ.Pal.Terr', 'Other Asia, nes']
EXCL_PARTNER = ['...', 'Special Category', 'World']

# ID columns for melting zip files
ID_VARS = ['Reporter', 'Partner', 'Product categories', 'Indicator Type', 'Indicator', 'Country_Code']


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in the zipped files, reshape with years in rows and indicator in cols
zip_file = ZipFile(r'.\inputs\wits_en_trade_summary_allcountries_allyears (3).zip')
df = ( pd.concat([pd.read_csv(zip_file.open(f.filename), 
                              encoding='ansi')
                    .assign(Country_Code = f.filename[3:6])
                    .query(f"`Indicator Type` in {INCL_INDICATOR_TYPE} " 
                           + f"& Reporter not in {EXCL_REPORTER} "
                           + f"& Partner not in {EXCL_PARTNER}")
                  for f in zip_file.infolist()])
         .melt(id_vars=ID_VARS, 
               var_name='Year') 
         .assign(value = lambda df_x: df_x['value'].astype(float),
                 Year = lambda df_x: pd.to_datetime('1/1/' + df_x['Year'])) 
         .pivot_table(index=[c for c in ID_VARS if c != 'Indicator'] + ['Year'], 
                      columns='Indicator', 
                      values='value', 
                      aggfunc='sum',
                      dropna=False)
         .reset_index()
         .rename(columns={ 'Country_Code' : 'Country Code' })
         .assign(Reporter = lambda df_x: df_x['Reporter'].str.strip()) )


# read in the country codes and split the lat/lon
df_codes = ( pd.read_csv(r'.\inputs\countries-codes.csv', sep=';')
               .assign(geo_point_2d = lambda df_x: df_x['geo_point_2d'].str.split(','))
               .assign(Latitude = lambda df_x: df_x['geo_point_2d'].str[0],
                       Longitude = lambda df_x: df_x['geo_point_2d'].str[1])
               [['ISO3 CODE', 
                 'LABEL EN', 
                 'Latitude', 
                 'Longitude']]
               .rename(columns={ 'ISO3 CODE' : 'Country Code'}) )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# join to get lat/lons
df = ( df.merge(df_codes[['Country Code', 'Latitude', 'Longitude']],
                on='Country Code',
                how='left')
         .merge(df_codes.rename(columns={ 'LABEL EN' : 'Partner' }),
                on='Partner',
                how='left',
                suffixes=['', '_Partner']) )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2023-14.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

pd.set_option('display.max_columns', 20)
pd.set_option('display.width', 1000)

solution_files = [r'.\outputs\World Imports and Exports.csv']
my_files = [r'.\outputs\output-2023-14.csv']
unique_cols = [['Reporter', 'Partner', 'Year', 'Indicator Type', 'Product categories']]


col_order_matters = False
round_dec = 6

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)


dfmine = pd.read_csv(my_files[0])
dfsol = pd.read_csv(solution_files[0])
sorted(dfsol['Reporter'].unique())
dfsol[dfsol['Partner']=='United Kingdom']


dfmine[dfmine['Partner']=='United Kingdom']
