# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 48 - Tiddlywinks Tidy
https://preppindata.blogspot.com/2022/11/2022-week-48-tiddlywinks-tidy.html

- Input the data
- Extract the Event id from the Event field
- Parse the competitor field into Competitor and Association
- For the first Games Output:
  - Reshape the data so we have a row per Game for each Event id and Competitor
  - Potouts are denoted by a * in the Score field. Add a boolean field to indicate whether there has been a Potout
  - Clean the Score field so that fractions are translated to decimals 
    - e.g. 2½ should be 2.5
- For the second Results Output:
  - Remove the Games fields
  - Clean the Points field so that fractions are translated to decimals 
    - e.g. 2½ should be 2.5
  - Extract the Event Start Date from the description and translate it to a date data type
  - Ensure the field names are easy to understand
- Output the datasets as separate sheets in the same Excel file

Author: Kelly Gilbert
Created: 2023-03-02
Requirements:
  - input dataset:
      - International Federation of Tiddlywinks Associations World Singles Results.csv
  - output dataset (for results check only):
      - Tiddlywinks.xlsx
"""


import pandas as pd


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def clean_score(scores, replace_regex_dict):
    """
    replaces fraction characters and converts to float
    """
    
    return ( scores.str.replace('*', '', regex=False)
                   .replace(replace_regex_dict, regex=True)
                   .astype(float) )


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\International Federation of Tiddlywinks Associations World Singles Results.csv', 
                 parse_dates=[], 
                 dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# extract the event ID and competitor info
df['Event id'] = df['event'].str.extract('.*?(\d+)$').astype(int)
df[['Competitor Name', 'Association']] = df['Competitors'].str.extract('(.*?) \((.*)\)')


# ---------- output #1 (game detail) ----------
fractions = { '(.*)½.*' : r'\1.5',
              '(.*)⅓.*' : r'\1.33',
              '(.*)⅔.*' : r'\1.67' }

# melt games into rows and filter out nulls
df_out1 = ( df.melt(id_vars=['Event id', 'Competitor Name', 'note'], 
                    value_vars=[c for c in df.columns if c[0]=='G'],
                    value_name='Score',
                    var_name='Game Order')
              .query("Score == Score") )

# flag potouts and fix fractions in score
df_out1['Potout'] = df_out1['Score'].str.contains('*', regex=False)
df_out1['Score'] = clean_score(df_out1['Score'], fractions)


# ---------- output #2 (game detail) ----------

renames = { 'W' : 'Wins',
            'L' : 'Losses',
            'T' : 'Ties',
            'description' : 'Event Description',
            'Pts' : 'Points',
            'event' : 'Event' }

# remove the game columns and rename columns
df_out2 = ( df.drop(columns=[c for c in df.columns if c[0]=='G'])
              .rename(columns=renames) )

# clean points and extract the event date
df_out2['Points'] = clean_score(df_out2['Points'], fractions)
df_out2['Event Start Date'] = ( pd.to_datetime(df_out2['Event Description']
                                                   .str.extract('(\d+ .*? \d{4}).*', expand=False))
                                                   .dt.strftime('%Y-%m-%d') )
                                                   

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

cols1 = ['Event id', 'Game Order', 'Competitor Name', 'Score', 'Potout', 'note']

cols2 = ['Event id', 'Competitor Name', 'Event', 'Event Start Date', 'Event Description', 
         'Association', 'Points', 'Wins', 'Losses', 'Ties']

with pd.ExcelWriter(r'.\outputs\output-2022-48.xlsx') as w:
    df_out1.to_excel(w, sheet_name='Games', index=False, columns=cols1)
    df_out2.to_excel(w, sheet_name='Results', index=False, columns=cols2)
    

#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked using Alteryx this week