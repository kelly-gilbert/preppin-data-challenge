# -*- coding: utf-8 -*-
"""
WORKING



Created on Sun Sep 11 14:43:12 2022

@author: gilbe
"""



import glob
import pandas as pd
from numpy import nan, where
import os
import re


# --------------------------------------------------------------------------------------------------
# import files
# --------------------------------------------------------------------------------------------------

# import the regex lookup file
df_regex = pd.read_csv(r'C:\Users\gilbe\projects\preppin-data-challenge\utilities\regex_lookup_python.csv')

# import the .py files
py_files = glob.glob(r'C:\Users\gilbe\projects\preppin-data-challenge\**\*-????-??.py', recursive=True)
py_contents = [open(f, encoding='utf-8').read() for f in py_files]

df = pd.DataFrame({'filepath' : py_files, 'contents' : py_contents})
df[['year', 'week']] = df['filepath'].str.extract(r'.*preppin-data-(\d{4})-(\d{2}).py').astype(float)


# --------------------------------------------------------------------------------------------------
# import files
# --------------------------------------------------------------------------------------------------

# cross join weekly py file contents with the regex lookup
df_all = df.merge(df_regex, how='cross')


# if the code string matches the regex, return a code snippet; otherwise nan
df_all['code_snippet'] = [c[max(0, x.span()[0]-20) : min(len(c), x.span()[1]+ 20)] 
                          if (x := re.search(r, c.lower())) != None else nan
                          for c,r in zip(df_all['contents'], df_all['Regex'])]


# output the matches for review
( df_all[df_all['code_snippet'].notna()].sort_values(by=['Category', 'Function/Method/Concept'])
      [['year', 'week', 'Category', 'Function/Method/Concept', 'code_snippet', 'May Overcount']]
      .to_csv(r'C:\Users\gilbe\projects\preppin-data-challenge\utilities\output.csv', index=False) )



# output possible over matches


# ouptput possible under matches
df_regex[df_regex['May Undercount']==1][['Category', 'Function/Method/Concept', 'Regex']]








# parse actual weeks
df_all = ( df.merge(df_regex, how='cross')
             .assign(year_week=lambda df_x: df_x['Weeks Used'].replace(':', '').str.split('\s+'))
             .explode('year_week')
             .assign(year=lambda df_x: pd.Series(where(~df_x['year_week'].str.contains('W'),
                                             df_x['year_week'], nan)).ffill(),
                     week=lambda df_x: where(df_x['year_week'].str.startswith('W'),
                                             df_x['year_week'].str.replace('W', ''),0).astype(int))
         )


# --------------------------------------------------------------------------------------------------
