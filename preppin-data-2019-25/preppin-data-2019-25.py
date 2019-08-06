# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2019-25

Clean and reshape data on Ben Howard and Ed Sheeran concerts from 
concertarchives.org, in preparation for Tableau Workout Wednesday 2019-31.

While it may have been easier or more efficient to perform some of these 
operations in-database, I wanted to challenge myself to perform all of 
the operations using pandas for my own practice.

https://preppindata.blogspot.com/2019/07/2019-week-25-when-pd-met-workout.html

Author: Kelly Gilbert
Created: 2019-08-03
Requirements: datasets Wow _ PD data set.xlsx and LongLats.csv
"""


import pandas as pd


#------------------------------------------------------------------------------
# Read in and investigate the files
#------------------------------------------------------------------------------
df_lat_lon = pd.read_csv('LongLats.csv')
df_lat_lon.head()
df_lat_lon.describe()
df_lat_lon.count()

df_concerts = pd.read_excel('Wow _ PD data set.xlsx')
df_concerts.head()
df_concerts.describe()    # 1545 records
df_concerts.count()


#------------------------------------------------------------------------------
# Join the files
#------------------------------------------------------------------------------

df_joined = pd.merge(df_concerts, df_lat_lon, on='Location', how='left')
#df_joined.describe()     # 1545 records
#df_joined.count()


#------------------------------------------------------------------------------
# Split the lon/lat field
#------------------------------------------------------------------------------

# ideally, the split would occur before joining, but I kept the split here 
#   to retain the order of steps from the challenge
df_latlon_split = df_joined.LongLats.str.extract('(?P<Longitude>[\d\.\-]+), (?P<Latitude>.*$)')
#df_latlon_split.head()

# add the split columns to the joined table, and drop the old column
df_joined = pd.merge(df_joined, df_latlon_split, left_index=True, right_index=True)

df_joined = df_joined.drop(['LongLats'], axis=1)
#df_joined.count()


#------------------------------------------------------------------------------
# Split the concert field
#------------------------------------------------------------------------------

# replace null values in the concert field with empty string
df_joined['Concert'] = df_joined['Concert'].fillna('')

# create a new dataframe with the concert ID and concert name
#    only including concert names with a slash
df_artist = df_joined[['ConcertID', 'Concert']][df_joined['Concert'].str.contains('/')]
8#df_artist.head()
#df_artist.count()

# create a new dataframe with the artists split into rows, using ConcertID
# as an index
df_artist = pd.DataFrame(df_artist.Concert.str.split(' / ').tolist(), \
                                index=df_artist.ConcertID).stack()

# make ConcertID a column and rename the fields
df_artist = df_artist.reset_index([0, 'ConcertID'])
df_artist.columns = ['ConcertID', 'Fellow Artists']
#df_artist.head()
#df_artist.count()

# remove Ben Howard, Ed Sheeran, and blanks
df_artist = df_artist[~df_artist['Fellow Artists'].isin(['Ben Howard', 'Ed Sheeran', ''])]
#df_artist.count()

# merge the new table with the main table into a new table
# the solution expects at least one row for Ben Howard or Ed Sheeran, plus
# rows for any Fellow Artists
df_artist = pd.merge(df_joined, df_artist, on='ConcertID')
#df_artist.count()

# union the new table with the primary table
df_joined['Fellow Artists'] = ''
df_final = pd.concat([df_joined, df_artist], ignore_index=True)
#df_final.count()


#------------------------------------------------------------------------------
# Remove duplicates
#------------------------------------------------------------------------------

# create a key field to identify unique records
df_final['unique_key'] = df_final['Artist'].fillna('') + '|' \
                          + df_final['Concert Date'].dt.strftime('%Y-%m-%d') + '|' \
                          + df_final['Concert'].fillna('') + '|' \
                          + df_final['Location'].fillna('') + '|' \
                          + df_final['Venue'].fillna('') + '|' \
                          + df_final['Fellow Artists'].fillna('')

df_final['unique_key'] = df_final['unique_key'].str.lower()
#df_final.head()

# delete duplicates based on the unique key
df_final = df_final.drop_duplicates(subset=['unique_key'], keep='first')
#df_final.count()

# remove the key
df_final = df_final.drop(columns=['unique_key', 'ConcertID'])
#df_final.count()


#------------------------------------------------------------------------------
# Add the home long/lat for each artist
#------------------------------------------------------------------------------

# create a dataframe of the home locations
df_hometowns = pd.DataFrame({
    'Artist':['Ed Sheeran', 'Ben Howard'],
    'Hometown':['Framlingham', 'Totnes'],
    'Home Longitude':[1.34234, -3.685109],
    'Home Latitude':[52.222283, 50.434792]
    })
df_hometowns.head()

# merge the hometowns dataset with the main dataset
df_final = pd.merge(df_final, df_hometowns, on='Artist')
df_final.count()
df_final.head()

#------------------------------------------------------------------------------
# Output the file
#------------------------------------------------------------------------------
df_final.to_csv(path_or_buf='output-2019-25.csv', index=False)
