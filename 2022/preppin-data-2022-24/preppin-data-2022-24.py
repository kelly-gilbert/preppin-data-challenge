# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 24 - Longest Flights
https://preppindata.blogspot.com/2022/06/2022-week-24-longest-flights.html

- Input the data
- Remove the airport names from the From and To fields
  - e.g. New York-JFK should just read New York
- Create a Route field which concatenates the From and To fields with a hyphen
  - e.g. Dubai - Dallas
- Split out the Distance field so that we have one field for the Distance in km and one field for the Distance in miles
  - Ensure these fields are numeric
- Rank the flights based on Distance
  - Use a dense rank in order to match the wikipedia page
- The Scheduled duration is a Date/Time data type. Change this to a string so that we only keep the time element
- Update the First flight field to be a date
- Join on the lat & longs for the From and To cities
- Output the data

Author: Kelly Gilbert
Created: 2022-07-25
Requirements:
  - input dataset:
      - 2022W24 Inputs.xlsx
  - output dataset (for results check only):
      - 2022W24 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function to compare my results to the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\2022W24 Inputs.xlsx') as xl:
    df_flights = pd.read_excel(xl, sheet_name='Non-stop flights', parse_dates=['First flight'], 
                               dtype={'Scheduled duration' : str})
    df_cities = pd.read_excel(xl, sheet_name='World Cities')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# remove the airport names from the From and To fields
df_flights[['From', 'To']] = df_flights[['From', 'To']].replace('[-–/].*', '', regex=True)


# create a Route field which concatenates the From and To fields with a hyphen
df_flights['Route'] = df_flights['From'] + ' - ' + df_flights['To'] 


# split out the Distance field so that we have one field for the Distance in km 
# and one field for the Distance in miles
df_flights[['Distance - km', 'Distance - mi']] = ( df_flights['Distance']
                                                      .str.extract('([\d\,]+) km \(([\d\,]+) mi.*')
                                                      .replace(',', '', regex=True)
                                                      .astype(int)
                                                 )


# rank the flights based on Distance
df_flights['Rank'] = df_flights['Distance - km'].rank(method='dense', ascending=False)


# change scheduled duration to a string so that we only keep the time element
# this was done with the parse_dates parameter in read_excel, above


# update the First flight field to be a date
# this was done with the dtype parameter in read_excel, above


# join to get the lat & longs for the From and To cities
df_out = ( df_flights.merge(df_cities, left_on='From', right_on='City', how='left')
                     .merge(df_cities, left_on='To', right_on='City', how='left')
                     .rename(columns={'Lat_x' : 'From Lat', 'Lng_x' : 'From Lng',
                                      'Lat_y' : 'To Lat', 'Lng_y' : 'To Lng'})
                     .drop(columns=['City_x', 'City_y', 'Distance'])
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-24.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W24 Output.csv']
my_files = [r'.\outputs\output-2022-24.csv']
unique_cols = [['From', 'To', 'Airline']]
col_order_matters = False
round_dec = 6

output_check(solution_files, my_files, unique_cols, col_order_matters=col_order_matters)
