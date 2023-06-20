# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 06 - DSB Customer Ratings
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


from numpy import where
import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = ( pd.read_csv(r'.\inputs\DSB Customer Survery.csv')
         .melt(id_vars='Customer ID',
               value_name = 'Rating')
         .query("not variable.str.contains('Overall Rating')", engine='python')
     )
     

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split the platform and question
df[['Platform', 'Question']] = df['variable'].str.split(' - ', expand=True)


# calculate the average for each customer/platform
df_cust = ( df.groupby(['Customer ID', 'Platform'], as_index=False)['Rating'].mean()
              .pivot_table(index='Customer ID',
                           columns='Platform',
                           values='Rating',
                           aggfunc='mean')
          )


# calculate the platform difference and category
df_cust['Diff'] = df_cust['Mobile App'] - df_cust['Online Interface']

df_cust['Preference'] = where(df_cust['Diff'] <= -2, 'Online Interface Superfan',
                        where(df_cust['Diff'] <= -1, 'Online Interface Fan',
                        where(df_cust['Diff'] < 1, 'Neutral',
                        where(df_cust['Diff'] < 2, 'Mobile App Fan',
                              'Mobile App Superfan'))))


# % by category
s_out = ( df_cust['Preference'].value_counts(normalize=True)
              .rename_axis('Preference')
              .rename('% of Total')
              .apply(lambda s: round(s*100, 1))
        )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

s_out.to_csv(r'.\outputs\output-2023-06.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week
print(pd.read_csv(r'.\outputs\output-2023-06.csv'))
