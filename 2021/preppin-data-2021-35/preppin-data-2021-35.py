# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 35 - Picture Perfect
https://preppindata.blogspot.com/2021/09/2021-week-35-picture-perfect.html

- Input the data
- Split up the sizes of the pictures and the frames into lengths and widths
  Remember an inch is 2.54cm
- Frames can always be rotated, so make sure you know which is the min/max side
- See which pictures fit into which frames
- Work out the area of the frame vs the area of the picture and choose the frame with the smallest
  excess
- Output the data

Author: Kelly Gilbert
Created: 2021-09-02
Requirements:
  - input dataset:
      - Pictures Input.xlsx
  - output dataset (for results check only):
      - (no output file this week)
"""

from numpy import where
from pandas import ExcelFile, merge, read_excel


def parse_sizes(s):
    """
    parses the a x b size strings, converts to centimeters, and calculates the area
    input: a series of strings
    output: a dataframe containing three columns: Max Side, Min Side, and Area
    """
    df = s.str.extract(r'(\d+)(\S+)(?: x )?(\d+)?(\S+)?')
    
    # convert to centimeters
    df[0] = df[0].astype(float) * where(df[1] == '"', 2.54, 1)
    df[2] = where(df[2].isna(), df[0], df[2]).astype(float) * where(df[1] == '"', 2.54, 1)
    
    # find largest size
    df['Max Side'] = where(df[0] >= df[2], df[0], df[2])
    df['Min Side'] = where(df[0] < df[2], df[0], df[2])
    df['Area'] = df['Max Side'] * df['Min Side']
    
    return df[['Max Side', 'Min Side', 'Area']]


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\inputs\Pictures Input.xlsx') as xl:
    p = read_excel(xl, 'Pictures')
    f = read_excel(xl, 'Frames').drop_duplicates().rename(columns={'Size' : 'Frame'})


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split up the sizes of the pictures and the frames into lengths and widths
p[['Max Side', 'Min Side', 'Area']] = parse_sizes(p['Size'])
f[['Max Side', 'Min Side', 'Area']] = parse_sizes(f['Frame'])


# all combinations of pictures and frames
df = p.assign(key=1).merge(f.assign(key=1), how='inner', on='key', suffixes=['', '_f'])\
      .drop('key', 1)


# find valid picture/frame combinations with the smallest area difference
df = df.loc[(df['Max Side'] <= df['Max Side_f']) & (df['Min Side'] <= df['Min Side_f'])]
df['Area_diff'] = df['Area_f'] - df['Area']
df = df[df['Area_diff'] == df.groupby(['Picture'])['Area_diff'].transform('min')]


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2021-35.csv', index=False, 
          columns=['Picture', 'Frame', 'Max Side', 'Min Side'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week

from pandas import read_csv
dfs = read_csv(r'.\outputs\output-2021-35.csv')
dfs
