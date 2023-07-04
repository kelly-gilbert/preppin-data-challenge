# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 11 - Which customers are closest? (polars)
https://preppindata.blogspot.com/2023/03/2023-week-11-which-customers-are-closest.html

- Input the data
- Append the Branch information to the Customer information
- Transform the latitude and longitude into radians
- Find the closest Branch for each Customer
- Make sure Distance is rounded to 2 decimal places
- For each Branch, assign a Customer Priority rating, the closest customer having a rating of 1
- Output the data

Author: Kelly Gilbert
Created: 2023-07-04
Requirements:
  - input dataset:
      - DSB Customer Locations.csv
      - DSB Branches.csv
  - output dataset (for results check only):
      - Customer - Branch Match.csv
"""


from numpy import arccos, cos, radians, sin
import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def haversine(lat1, lon1, lat2, lon2):
    """
    returns an array of the haversine distance in miles. assumes coordinates are in degrees.
    """
    
    return 3963 * arccos((sin(radians(lat1)) * sin(radians(lat2))) 
                         + cos(radians(lat1)) * cos(radians(lat2)) 
                                 * cos(radians(lon2) - radians(lon1)))


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

df = ( # create all combinations of customer and branch
       pl.scan_csv(r'.\inputs\DSB Customer Locations.csv')
         .join(pl.scan_csv(r'.\inputs\DSB Branches.csv'),
               how='cross')
         
         # calculate haversine distance
         .with_columns(haversine(pl.col('Address Lat'), 
                                 pl.col('Address Long'),
                                 pl.col('Branch Lat'), 
                                 pl.col('Branch Long'))
                           .round(2)
                           .alias('Distance')
         )
         
         # keep the closest branch for each customer
         .sort('Distance', descending=False)
         .unique('Customer')
         
         # rank customers within the branch
         .with_columns(
             pl.col('Distance')
               .rank()
               .over('Branch')
               .cast(pl.Int16)
               .alias('Customer Priority')
         )
     )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.collect().write_csv(r'.\outputs\output-2023-11.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Customer - Branch Match.csv']
my_files = [r'.\outputs\output-2023-11.csv']
unique_cols = [['Branch', 'Customer']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
