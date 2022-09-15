# -*- coding: utf-8 -*-
"""
WORKING



Created on Sun Sep 11 14:43:12 2022

@author: gilbe
"""



import glob
import pandas as pd
from numpy import nan, where
import re


# --------------------------------------------------------------------------------------------------
# functions
# --------------------------------------------------------------------------------------------------

def make_snippet(string, start, end, margin=20):
    """returns a snippet of string starting at start-margin and ending at end_margin"""
    
    return string[max(0, start-margin) : min(len(string), end+margin)]
    



# --------------------------------------------------------------------------------------------------
# import files
# --------------------------------------------------------------------------------------------------

# import the regex lookup file
df_regex = pd.read_csv(r'.\utilities\regex_lookup_python.csv')

# import the .py files
py_files = glob.glob(r'**/preppin-data-????-*.py', recursive=True)
py_contents = [open(f, encoding='utf-8').read() for f in py_files]

# read into a dataframe and parse tye year/week
df = pd.DataFrame({'filepath' : py_files, 'contents' : py_contents})
df[['year', 'week']] = df['filepath'].str.extract(r'.*preppin-data-(\d{4})-(\d{2}).py').astype(float)

# ignore the part before the imports and after the output check and check for nans
df['contents'] = df['contents'].str.extract('.*?((?:from|import).*?)(?:[\s#-]*check results|$).*', flags=re.DOTALL)

if len(df_missing := df[df['contents'].isna()][['year', 'week']]) > 0:
    print(f'The following year/weeks did not parse properly:\n{df_missing}')


# --------------------------------------------------------------------------------------------------
# compare regex
# --------------------------------------------------------------------------------------------------

# cross join weekly py file contents with the regex lookup
df_all = df.merge(df_regex, how='cross')


# if the code string matches the regex, return a code snippet; otherwise nan
df_all['code_snippet'] = [make_snippet(c, *x.span(), margin=20) 
                          if (x := re.search(r.lower(), c.lower(), flags=re.DOTALL)) != None 
                          else nan
                          for c,r in zip(df_all['contents'], df_all['Regex'])]

df_all = df_all.loc[df_all['code_snippet'].notna()]


# output the matches for review
( df_all.sort_values(by=['Category', 'Function/Method/Concept', 'year', 'week'])
      [['year', 'week', 'Category', 'Function/Method/Concept', 'code_snippet', 'May Overcount']]
      .to_csv(r'.\utilities\output.csv', index=False) )


# check for concepts that did not match any weeks
if len(df_missing := df_regex.loc[(~df_regex['Function/Method/Concept']
                                      .isin(df_all['Function/Method/Concept']))
                                  & (df_regex['Regex'] != 'xxx[Manual]xxx')]) > 0:
    print(f"The folowing concepts did not match any weeks:\n{df_missing[['Category', 'Function/Method/Concept']]}")


# output possible over matches for check



# ouptput possible under matches
df_regex[df_regex['May Undercount']==1][['Category', 'Function/Method/Concept', 'Regex']]


# --------------------------------------------------------------------------------------------------
# compare regex matches to manual matches
# --------------------------------------------------------------------------------------------------

# parse actual weeks
df_weeks = ( df_regex.assign(year_week=lambda df_x: df_x['Weeks Used'].replace(':', '').str.split('\s+'))
               .explode('year_week')
               .assign(year=lambda df_x: pd.Series(where(~df_x['year_week'].str.contains('W'),
                                                         df_x['year_week'], nan))
                                                       .ffill()
                                                       .str.replace(':', '', regex=False)
                                                       .astype(int),
                     week=lambda df_x: where(df_x['year_week'].str.startswith('W'),
                                             df_x['year_week'].str.replace('W', '', True),0)
                                          .astype(int))
               .drop(columns=['year_week', 'Weeks Used', 'Regex', 'May Overcount', 'May Undercount'])
               .query('week != 0')
           )

df_compare = ( df_all[['Category', 'Function/Method/Concept', 'year', 'week']]
                  .merge(df_weeks, on=['Category', 'Function/Method/Concept', 'year', 'week'], 
                         how='outer', indicator=True)
                  [['Category', 'Function/Method/Concept', 'year', 'week', '_merge']]
             )

print('Weeks in actuals, not in regex match:\n')
print(df_compare[df_compare['_merge']=='right_only'])

print('Weeks in regex_match, not in actuals:\n')
print(df_compare[df_compare['_merge']=='left_only'].drop(columns='_merge'))


# --------------------------------------------------------------------------------------------------









