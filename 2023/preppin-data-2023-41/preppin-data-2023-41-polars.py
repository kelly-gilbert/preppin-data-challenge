# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 41 - An International School
https://preppindata.blogspot.com/2023/10/2023-week-41-international-school.html

- Input Data 1 and Input Data 2
- Join both datasets on the Student ID (p.s. you shouldn't always listen to the 
  requirements :) )
- Group Values by Spelling to get rid of spelling mistakes in the Nationality 
  field
- Aggregate the dataset to get a count of students within each Nationality and 
  classroom
- Create a calculated field to output the Rank of each Nationality by classroom 
  in descending order. Follow this blog to learn how to rank in Tableau prep.
- Filter the Dataset to keep the first-ranking Nationality in each classroom
- Remove unnecessary fields 
- Output the data

Author: Kelly Gilbert
Created: 2023-12-03
Requirements:
  - Python 3.9+ for | dict operator
  - input datasets:
      - Student_Name.csv
      - Student_Nationality.csv
  - output dataset (for results check only):
      - NationalityOutput.xlsx - result.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

# (key) correct spelling : (value) list of misspellings
NAT_DICT = { 'Brasil' : [],
            'Canada' : [],
             'China' : ['Chyna'],
             'Egypt' : ['Egipt'],
             'France' : ['Frans'],
             'Germany' : [],
             'Italy' : [],
             'Mexico' : ['Meksiko'],
             'South Korea' : [],
             'Spain' : [],
             'USA' : []
             }


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

nat_lookup = {i : k for k,v in NAT_DICT.items() for i in v} | {k : k for k in NAT_DICT.keys()}

df_name = pd.read_csv(r'.\inputs\Student_Name.csv')
df_nat = ( pd.read_csv(r'.\inputs\Student_Nationality.csv')
             .assign(Nationality = lambda df_x:
                         df_x['Nationality'].replace(nat_lookup)
             )
         )

    
#---------------------------------------------------------------------------------------------------
# check the data
#---------------------------------------------------------------------------------------------------

# check for student IDs in the nationality table, but not in the name table
if (missing := df_nat[~df_nat['Student ID']
                          .isin(df_name['Student ID'].unique())]
                     ['Student ID']).any():
    print('The following Student IDs are in the nationality table, but not the name table:')
    print(missing, end=chr(10))


# check for student IDs in the name table, but not the nationality table
if (missing := df_name[~df_name['Student ID']
                           .isin(df_nat['Student ID'].unique())]
                      ['Student ID']).any():
    print('The following Student IDs are in the name table, but not the nationality table:')
    print(missing, end=chr(10))
    

# check for nationalities not in the lookup dict
if (missing:=[n for n in df_nat['Nationality'].unique() if n not in nat_lookup.keys()]):
    print('The following nationalities are missing from the lookup dict:')
    print(chr(10).join(missing), end=chr(10))


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------


# ---------- method 1: by the instructions (join)
df_out = ( df_nat
               .merge(df_name,
                      on='Student ID',
                      how='left')
               .groupby(['Nationality', 'Classroom'], as_index=False)
               ['Name'].count()
               .assign(nat_rank = lambda df_x:
                           df_x.groupby('Classroom')['Name'].transform('rank', 
                                                                       ascending=False,
                                                                       method='min'))
               .query("nat_rank==1")
               .drop(columns=['nat_rank'])
         )


# ---------- method 2 (no join)
df_out = ( df_nat
               .groupby(['Nationality', 'Classroom'], as_index=False)
               ['Student ID'].count()
               .assign(max_count = lambda df_x:
                           df_x.groupby('Classroom')['Student ID'].transform('max'))
               .query("`Student ID`==max_count", engine='python')
               .drop(columns=['max_count'])
               .rename(columns={'Student ID' : 'Name'})
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2023-38.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\NationalityOutput.xlsx - result.csv']
my_files = [r'.\outputs\output-2023-41.csv']
unique_cols = [['Classroom']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
