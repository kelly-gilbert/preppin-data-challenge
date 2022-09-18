# -*- coding: utf-8 -*-
"""
Build a regex lookup file to match Python concepts in code.

1 - Get a list of all existing Preppin' Data .py files
2 - Compare them to the regex lookups to get a list of concepts by week
3 - Parse the manually-built reference tables from github
4 - Compare the concept/weeks identified by regex to the manually-updated concept/weeks 


Author: Kelly Gilbert
Created: 2022-09-11

Requirements:
- Current working directory is the main preppin-data-challenge directory
- Regex lookup file (utilities\regex_lookup_python.csv)

"""


from os import chdir
chdir(r'C:\Users\gilbe\projects\preppin-data-challenge')


import glob
import pandas as pd
from numpy import NaN, where
import re


# --------------------------------------------------------------------------------------------------
# functions
# --------------------------------------------------------------------------------------------------

def make_snippet(string, start, end, margin=20):
    """returns a snippet of string starting at start-margin and ending at end_margin"""
    
    return string[max(0, start-margin) : min(len(string), end+margin)]


def print_mismatches(df, top_n=None):
    """prints mismatched year/week combinations for each concept"""
    
    counts = df['Function/Method/Concept'].value_counts()
       
    for i, v in counts.iloc[0 : min(top_n, len(counts))].iteritems():
        print(f'\n\n\n---------- {i} ({v})----------')
        
        yr_wks = ( df[df['Function/Method/Concept']==i][['year', 'week']]
                       .sort_values(by=['year', 'week']) )
        
        print(str(yr_wks))
    

# --------------------------------------------------------------------------------------------------
# import files
# --------------------------------------------------------------------------------------------------

# import the regex lookup file
df_regex = pd.read_csv(r'.\utilities\regex_lookup_python.csv')

# import the .py files
py_files = glob.glob(r'**/preppin-data-????-??/**/*.py', recursive=True)
py_contents = [open(f, encoding='utf-8').read() for f in py_files]


# read into a dataframe and parse tye year/week
df = pd.DataFrame({'filepath' : py_files, 'contents' : py_contents})
df[['year', 'week']] = df['filepath'].str.extract(r'.*preppin-data-(\d{4})-(\d{2}).*').astype(float)


# ignore the part before the imports and after the output check and check for nans
df['contents'] = df['contents'].str.extract('.*?((?:from|import).*?)(?:[\s#-]*check results|$).*', 
                                            flags=re.DOTALL)


if len(df_missing := df[df['contents'].isna()][['year', 'week']]) > 0:
    print(f'The following year/weeks did not parse properly:\n{df_missing}')


# --------------------------------------------------------------------------------------------------
# compare regex
# --------------------------------------------------------------------------------------------------

# cross join weekly py file contents with the regex lookup
df_all = df.merge(df_regex, how='cross')



# if the code string matches the regex, return a code snippet; otherwise nan
df_all['code_snippet'] = [make_snippet(c, *x.span(), margin=20) 
                          if (x := re.search(r, c.lower(), flags=re.DOTALL)) != None 
                          else NaN
                          for c,r in zip(df_all['contents'], df_all['Regex'])]

df_all = df_all.loc[df_all['code_snippet'].notna()]


# check for concepts that did not match any weeks
if len(df_missing := df_regex.loc[(~df_regex['Function/Method/Concept']
                                      .isin(df_all['Function/Method/Concept']))
                                  & (df_regex['Regex'] != 'xxx[Manual]xxx')]) > 0:
    print("The folowing concepts did not match any weeks:\n\n" +
          str(df_missing[['Category', 'Function/Method/Concept']]))


# --------------------------------------------------------------------------------------------------
# compare regex matches to manual matches
# --------------------------------------------------------------------------------------------------

# parse actual weeks
df_weeks = ( df_regex.assign(week=lambda df_x: df_x['Weeks Used'].str.split('\:?\s+W?0?'))
                 .explode('week')
                 .reset_index()
                 .assign(week = lambda df_x: df_x['week'].astype(int))
                 .assign(year = lambda df_x: pd.Series(where(df_x['week'] > 100, df_x['week'], None))
                                               .ffill())
                 .drop(columns=['Weeks Used', 'Regex', 'May Overcount', 'May Undercount'])
                 .query('week != year')
           )

df_compare = ( df_all[['Category', 'Function/Method/Concept', 'year', 'week', 'May Overcount', 'May Undercount']]
                  .merge(df_weeks, on=['Category', 'Function/Method/Concept', 'year', 'week'], 
                         how='outer', indicator=True)
                  [['Category', 'Function/Method/Concept', 'year', 'week', 'May Overcount', 
                    'May Undercount', '_merge']]
             )

df_compare['_merge'] = df_compare['_merge'].replace({'right_only' : 'in actual', 
                                                     'left_only' : 'in regex match'})



# check for weeks in manually-built table that were not matched by regex
print_mismatches(df_compare[(df_compare['_merge']=='in actual')], 20)


# check for weeks in regex matches that are labeled as possible overcounts
print_mismatches(df_compare[(df_compare['_merge']=='in regex match')
                            & (df_compare['May Overcount']==1)], 50)


# --------------------------------------------------------------------------------------------------
# output matches to file
# --------------------------------------------------------------------------------------------------

( df_compare[df_compare['_merge'] != 'in actual']
      .sort_values(by=['year', 'week', 'Category', 'Function/Method/Concept'])
      [['Category', 'Function/Method/Concept', 'year', 'week']]
      .to_csv(r'.\utilities\python_concept_assignments.csv', index=False)
)
