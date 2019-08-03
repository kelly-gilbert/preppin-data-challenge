# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2019-25

Clean and reshape data on Ben Howard and Ed Sheeran concerts from 
concertarchives.org, in preparation for Tableau Workout Wednesday 2019-31.

Author: Kelly Gilbert
Created: 2019-08-03
Requirements: datasets Wow _ PD data set.xlsx and LongLats.csv
"""


import pandas as pd


# read in the files
df_lat_lon = pd.read_csv('LongLats.csv')
df_lat_lon.head()
df_lat_lon.describe()
df_lat_lon.count()

df_concerts = pd.read_excel('Wow _ PD data set.xlsx')
df_concerts.head()
df_concerts.describe()    # 1545 records
df_concerts.count()


# join the files
df_joined = pd.merge(df_concerts, df_lat_lon, on='Location', how='left')
df_joined.describe()     # 1545 records
df_joined.count()

# split the lat/lon column using regex
# ideally, the split would occur before joining, but I wanted to retain
#    the order of steps from the challenge
df_latlon_split = df_joined.LongLats.str.extract('(?P<Longitude>[\d\.\-]+), (?P<Latitude>.*$)')
df_latlon_split.head()

# add the split columns to the joined table, and drop the old column
df_joined = pd.merge(df_joined, df_latlon_split, left_index=True, right_index=True)

df_joined = df_joined.drop(['LongLats'], axis=1)
df_joined.count()


#------------------------------------------------------------------------------
# Split the concert field
#------------------------------------------------------------------------------

# replace null values in the concert field with empty string
df_joined['Concert'] = df_joined['Concert'].fillna('')

# create a new dataframe with the artists split into rows, using ConcertID
# as an index
df_artist = pd.DataFrame(df_joined.Concert.str.split(' / ').tolist(), \
                                index=df_joined.ConcertID).stack()

# make ConcertID a column and rename the fields
df_artist = df_artist.reset_index([0, 'ConcertID'])
df_artist.columns = ['ConcertID', 'Fellow Artists']
df_artist.head()
df_artist.count()

# remove Ben Howard and Ed Sheeran
df_artist = df_artist[~df_artist['Fellow Artists'].isin(['Ben Howard', 'Ed Sheeran'])]
df_artist.count()

# merge the new table with the main table
df_joined = pd.merge(df_joined, df_artist, on='ConcertID', how='left')
df_joined.count()


#------------------------------------------------------------------------------
# Remove duplicates
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Add the home long/lat for each artist
#------------------------------------------------------------------------------




#------------------------------------------------------------------------------
# Output the file
#------------------------------------------------------------------------------




df_joined.iloc[0]

df_joined['Concert'].iloc[280:285,]
df_joined.iloc[283,]
