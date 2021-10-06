# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 40 - Animal Adoptions
https://preppindata.blogspot.com/2021/10/2021-week-40-animal-adoptions.html

- Input the data
- Remove the duplicated date field
- Filter to only cats and dogs (the other animals have too small a data sample)
- Group up the Outcome Type field into 2 groups:
    - Adopted, Returned to Owner or Transferred
    - Other
- Calculate the % of Total for each Outcome Type Grouping and for each Animal Type
- Output the data

Author: Kelly Gilbert
Created: 2021-10-06
Requirements:
  - input dataset:
      - Austin_Animal_Center_Outcomes.csv
"""


from numpy import where
from pandas import crosstab, read_csv

# used for testing outcome group data types only
from pandas import Series


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

usecols = ['Animal ID', 'Outcome Type', 'Animal Type']
df = read_csv(r'.\\inputs\\Austin_Animal_Center_Outcomes.csv', usecols=usecols)
df = df.loc[df['Animal Type'].isin(['Cat','Dog'])]


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# group up the Outcome Type field into 2 groups
group1 = ['Adoption', 'Transfer', 'Return to Owner']
df['Outcome Group'] = where(df['Outcome Type'].isin(group1),
                            'Adopted, Returned to Owner or Transferred', 
                            'Other')

# calculate the % of Total for each Outcome Type Grouping and for each Animal Type
final = (crosstab(df['Animal Type'], df['Outcome Group'], normalize='index')*100).round(1)\
        .reset_index()


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

final.to_csv(r'.\outputs\output-2021-40.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week
read_csv(r'.\\outputs\output-2021-40.csv')


#---------------------------------------------------------------------------------------------------
# testing different group data types -- not needed for the challenge
#---------------------------------------------------------------------------------------------------

df['Outcome Group (string)'] = where(df['Outcome Type'].isin(group1),
                                        'Adopted, Returned to Owner or Transferred', 'Other')
df['Outcome Group (int)'] = where(df['Outcome Type'].isin(group1), 0, 1)
df['Outcome Group (cat)'] = Series(where(df['Outcome Type'].isin(group1),
                                          'Adopted, Returned to Owner or Transferred', 'Other'))\
                                    .astype('category')
                                    
print('----- column size in MB -----')
print(df.memory_usage() / 1024**2)

