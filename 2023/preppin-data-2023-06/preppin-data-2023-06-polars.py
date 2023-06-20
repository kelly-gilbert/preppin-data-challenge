# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 06 - DSB Customer (polars)
https://preppindata.blogspot.com/ - challenge url goes here

- Input the data
- Reshape the data so we have 5 rows for each customer, with responses for the Mobile App and Online 
  Interface being in separate fields on the same row
- Clean the question categories so they don't have the platform in from of them
  - e.g. Mobile App - Ease of Use should be simply Ease of Use
- Exclude the Overall Ratings, these were incorrectly calculated by the system
- Calculate the Average Ratings for each platform for each customer 
- Calculate the difference in Average Rating between Mobile App and Online Interface for each customer
- Catergorise customers as being:
  - Mobile App Superfans if the difference is greater than or equal to 2 in the Mobile App's favour
  - Mobile App Fans if difference >= 1
  - Online Interface Fan
  - Online Interface Superfan
  - Neutral if difference is between 0 and 1
- Calculate the Percent of Total customers in each category, rounded to 1 decimal place
- Output the data

Author: Kelly Gilbert
Created: 2023-06-19
Requirements:
  - input dataset:
      - DSB Customer Survery.csv
  - output dataset (for results check only):
      - N/A - checked by visual inspection
"""


import polars as pl


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

df = ( pl.read_csv(r'.\inputs\DSB Customer Survery.csv')
         .melt(id_vars='Customer ID',
               value_name = 'Rating')
         
         # remove overall ratings
         .filter(~pl.col('variable').str.contains('Overall Rating'))
         
         # split platform type
         .with_columns(pl.col('variable').str.split(' - ').list.first().alias('Platform'))
         
         # average rating by customer and platform
         .pivot(index='Customer ID',
                columns='Platform',
                values='Rating',
                aggregate_function='mean')
         
         # diff between platforms
         .with_columns((pl.col('Mobile App') - pl.col('Online Interface')).alias('Diff'))
         
         # categories
         .with_columns( 
             pl.when(pl.col('Diff') <= -2).then('Online Interface Superfan')
               .when(pl.col('Diff') <= -1).then('Online Interface Fan')
               .when(pl.col('Diff') < 1).then('Neutral')
               .when(pl.col('Diff') < 2).then('Mobile App Fan')
               .otherwise('Mobile App Superfan') 
               .alias('Preference')
         )
         
         # output the counts
         .groupby('Preference')
         .agg(pl.col('Customer ID').count().alias('Cust Count'))
         .select([pl.col('Preference'),
                  (pl.col('Cust Count') / pl.sum('Cust Count') * 100)
                     .round(1)
                     .alias('% of Total')]
         )
      )
     

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.write_csv(r'.\outputs\output-2023-06.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week
print(pl.read_csv(r'.\outputs\output-2023-06.csv'))
