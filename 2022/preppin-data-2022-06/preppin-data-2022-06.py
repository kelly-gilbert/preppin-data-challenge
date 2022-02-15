# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 6 - 7 letter Scrabble Words
https://preppindata.blogspot.com/2022/02/2022-week-6-7-letter-scrabble-words.html

- Input the data
- Parse out the information in the Scrabble Scores Input so that there are 3 fields:
    - Tile
    - Frequency
    - Points
- Calculate the % Chance of drawing a particular tile and round to 2 decimal places
- Frequency / Total number of tiles
- Split each of the 7 letter words into individual letters and count the number of occurrences of 
  each letter
- Join each letter to its scrabble tile 
- Update the % chance of drawing a tile based on the number of occurrences in that word
    - If the word contains more occurrences of that letter than the frequency of the tile, set the 
      probability to 0 - it is impossible to make this word in Scrabble
    - Remember for independent events, you multiple together probabilities i.e. if a letter appears 
      more than once in a word, you will need to multiple the % chance by itself that many times
- Calculate the total points each word would score
- Calculate the total % chance of drawing all the tiles necessary to create each word
- Filter out words with a 0% chance
- Rank the words by their % chance (dense rank)
- Rank the words by their total points (dense rank)
- Output the data

Author: Kelly Gilbert
Created: 2022-02-09
Requirements:
  - input dataset:
      - 7 letter words.xlsx
  - output dataset (for results check only):
      - 7 letter output.csv
"""


import decimal as d
from numpy import where
import pandas as pd


# precision of Decimal operations
d.getcontext().prec = 14


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\7 letter words.xlsx') as xl:
    df_words = pd.read_excel(xl, sheet_name='7 letter words')
    df_scores = pd.read_excel(xl, sheet_name='Scrabble Scores')
    
    
#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split the point and tile info, split tiles into rows, split tile letter and frequency
df_scores = df_scores['Scrabble'].str.extract('(?P<Points>\d+) points?:\s+(?P<Tile>.*)')\
            .assign(Tile=lambda df_x: df_x['Tile'].str.split(','))\
            .explode('Tile')\
            .assign(Frequency=lambda df_x: df_x['Tile'].str.extract(r'.*×(\d+)').astype(int),
                    Tile=lambda df_x: df_x['Tile'].str.lower().str.extract(r'\s*(.*?)\s+.*'),
                    Points=lambda df_x: df_x['Points'].astype(int))


# calculate the % Chance of drawing a particular tile and round to 2 decimal places
df_scores['Tile Chance'] = (df_scores['Frequency'] / df_scores['Frequency'].sum()).round(2).apply(d.Decimal)


# count of letters in each word
df_letters = df_words.assign(Tile=lambda df_x: df_x['7 letter word'].str.lower().str.findall('(.)'))\
                     .explode('Tile')\
                     .groupby(['7 letter word', 'Tile'], as_index=False).agg(Count=('Tile', 'size'))


# join the words and letters, calculate the % chance
df_letters = df_letters.merge(df_scores, on='Tile')\
                       .assign(Total_Chance=lambda df_x: where(df_x['Count'] > df_x['Frequency'], 0,
                                                               df_x['Tile Chance'] ** df_x['Count']),
                               Total_Points=lambda df_x: where(df_x['Count'] > df_x['Frequency'], 0,
                                                               df_x['Points'] * df_x['Count']))


# group by word, filtering out impossible words
df_out = df_letters.groupby('7 letter word')\
                   .filter(lambda df_x: df_x['Total_Chance'].min() > 0.0)\
                   .groupby('7 letter word', as_index=False)\
                   .agg(Total_Chance=('Total_Chance', 'prod'),
                        Total_Points=('Total_Points', 'sum'))\
                   .rename(columns={'Total_Chance' : '% Chance', 'Total_Points' : 'Total Points'})

df_out['Points Rank'] = df_out['Total Points'].rank(method='dense', ascending=False).astype(int)
df_out['Likelihood Rank'] = df_out['% Chance'].rank(method='dense', ascending=False).astype(int)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-06.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# NOTE: my Likelihood Rank does not match the solution due to floating point math

solution_files = ['7 letter output.csv']
my_files = ['output-2022-06.csv']
unique_cols = [['7 letter word']]
col_order_matters = False
round_dec = 14

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_sol = pd.read_csv('.\\outputs\\' + solution_file)
    df_mine = pd.read_csv('.\\outputs\\' + my_files[i])

    # are the columns the same?
    solution_cols = list(df_sol.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_sol.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
        print('\n\n')
    else:
        print('Columns match\n')
        col_match = True


    # are the values the same? (only check if the columns matched)
    if col_match:
        errors = 0
        df_compare = df_sol.merge(df_mine, how='outer', on=unique_cols[i],
                                  suffixes=['_sol', '_mine'], indicator=True)
        
        # extra/missing records
        if len(df_compare[df_compare['_merge'] != 'both']) > 0:
            print('*** Missing or extra records ***\n')
            print('In solution, not in mine:\n')
            print(df_compare[df_compare['_merge'] == 'left_only'][unique_cols[i]])
            print('\n\nIn mine, not in solution:\n')
            print(df_compare[df_compare['_merge'] == 'right_only'][unique_cols[i]]) 
            errors += 1

        # for the records that matched, check for mismatched values
        for c in [c for c in df_sol.columns if c not in unique_cols[i]]:
            if 'float' in df_compare[f'{c}_sol'].dtype.name:
                df_compare[f'{c}_sol'] = df_compare[f'{c}_sol'].round(round_dec)
                df_compare[f'{c}_mine'] = df_compare[f'{c}_mine'].round(round_dec)
                
            unmatched = df_compare[(df_compare['_merge']=='both')
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]
            if len(unmatched) > 0:
                print(f'*** Values do not match: {c} ***\n')
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                errors += 1
        
        if errors == 0:
            print('Values match')

    print('\n')  


#---------------------------------------------------------------------------------------------------
# example of ranking differences
#---------------------------------------------------------------------------------------------------

pd.set_option('display.width', 200)
pd.set_option('display.max_columns', 10)
    
df_compare[df_compare['Likelihood Rank_mine']==3]\
    [['7 letter word', '% Chance_sol', '% Chance_mine', 'Likelihood Rank_sol', 'Likelihood Rank_mine']]
