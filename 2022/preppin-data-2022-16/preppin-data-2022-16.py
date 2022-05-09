# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 16 - challenge title goes here
https://preppindata.blogspot.com/2022/04/2022-week-16-restaurant-orders.html

- Input the data
- Reshape the Orders table so that we have 3 columns:
    - Guest name
    - Dish
    - Selections (containing 🗸 or null)
- Extract the course name from the Dish field
- Group these so that Starter and Starters are treated the same, for example
- Fill down the course name for each Guest (hint)
- It may help to bring in the Recipe ID from the Lookup Table 
- Where the Dish contains the Course name, it may be helpful to replace the Recipe ID in the following way:
    Starters = 1
    Mains = 2 
    Dessert = 3
- Filter out where the Dish = Course
- Filter out Dishes which have not been selected
- Output the Data

Author: Kelly Gilbert
Created: 2022-05-08
Requirements:
  - input dataset:
      - Menu Input.xlsx
  - output dataset (for results check only):
      - N/A
  - output_check module (for results check only)

"""

from numpy import NaN, where
import pandas as pd


COURSES = {'Main' : 'Mains', 'Starter' : 'Starters', 'Desserts' : 'Dessert'}


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\Menu Input.xlsx') as xl:
    # drop totally blank columns
    df_orders = pd.read_excel(xl, 'Orders')\
                  .dropna(how='all', axis=1)
    
    df_lookup = pd.read_excel(xl, 'Lookup Table')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# rename the columns name_Dish and name_Selection
df_orders.columns = [f'{df_orders.columns[i-1]}_Selection' if 'Unnamed' in c else f'{c}_Dish'
                     for i, c in enumerate(df_orders.columns)]


# melt original columns into rows, split the column names into guest name and dish or selection,
# pivot dish/selection into columns
# fill the course name down
# join to lookup to get the recipe id
df_out = \
    df_orders.reset_index()\
             .melt(id_vars='index')\
             .assign(Guest=lambda df_x: df_x['variable'].str.extract('(.*?)\_.*'),
                     Type=lambda df_x: df_x['variable'].str.extract('.*?\_(.*)'))\
             .pivot_table(index=['Guest', 'index'], values='value', columns='Type', aggfunc='first')\
             .reset_index()\
             .assign(Course=lambda df_x: pd.Series(
                 where(df_x['Dish'].str.match('|'.join(list(COURSES.keys()) + list(COURSES.values()))),
                       df_x['Dish'].replace(COURSES), NaN )).ffill())\
             .dropna(subset=['Selection'])\
             .drop(columns=['Selection', 'index'])\
             .merge(df_lookup, how='left', on='Dish')
    

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-16.csv', index=False, 
              columns=['Guest', 'Course', 'Recipe ID', 'Dish'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week
