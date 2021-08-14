# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 30 - Lift Your Spirits
https://preppindata.blogspot.com/2021/07/2021-week-30-lift-your-spirits.html

- Input the data
- Create a TripID field based on the time of day
  - Assume all trips took place on 12th July 2021
- Calculate how many floors the lift has to travel between trips
  - The order of floors is B, G, 1, 2, 3, etc.
- Calculate which floor the majority of trips begin at - call this the Default Position
- If every trip began from the same floor, how many floors would the lift need to travel to begin 
  each journey?
  e.g. if the default position of the lift were floor 2 and the trip was starting from the 4th floor,
  this would be 2 floors that the lift would need to travel
- How does the average floors travelled between trips compare to the average travel from the default position?
- Output the data

Author: Kelly Gilbert
Created: 2021-08-13
Requirements:
  - input dataset:
      - 2021W30.csv
  - no output dataset this week
"""



from pandas import DataFrame, read_csv, to_datetime


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\inputs\2021W30.csv')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

floor_map = { 'B' : -1, 'G' : 0}

# create a TripID field based on the time of day; assume all trips took place on 12th July 2021
# if there are multiple records per timestamp, the original record order is maintained
df['trip_dtt'] = to_datetime('2021-07-12 ' + df['Hour'].astype(str) + ':' + df['Minute'].astype(str), 
                            format='%Y-%m-%d %H:%M')
df = df.reset_index().sort_values(by=['trip_dtt', 'index']).rename(columns={'index' : 'trip_id'})


# calculate how many floors the lift has to travel between trips
df['From'] = df['From'].replace(floor_map).astype(int)
df['To'] = df['To'].replace(floor_map).astype(int)
df['floors'] = abs(df['From'].shift(-1) - df['To'])


# calculate which floor the majority of trips begin at - call this the Default Position
default_position = df.groupby('From')['To'].size().idxmax()


# if every trip began from the same floor, how many floors would the lift need to travel to begin 
# each journey?
df['floors_from_dp'] = abs(df['From'].shift(-1) - default_position)


# summarize output
if default_position in floor_map.values():
    default_position = {v:k for k, v in floor_map.items()}[default_position]
    
df_out = DataFrame( { 'Default Position' : [default_position],
                      'Avg travel from default position' : [round(df['floors_from_dp'].mean(), 2)],
                      'Avg Travel between trips currently' : [round(df['floors'].mean(), 2)],
                    } )
df_out['Difference'] = round((df_out['Avg travel from default position']\
                              - df_out['Avg Travel between trips currently']), 2)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2021-30.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week
