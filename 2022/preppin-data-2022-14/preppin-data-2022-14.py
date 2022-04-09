# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 14 - House of Games Winners
https://preppindata.blogspot.com/2022/04/2022-week-14-house-of-games-winners.html

- Input the data
- Only keep relevant fields and rename certain fields to remove duplication
    - Ser. becomes Series
    - Wk. becomes Week
    - T becomes Tu
    - T 1 becomes Th
    - Total becomes Score
    - Week becomes Points
    - Week 1 becomes Rank
- Filter the data to remove Series that have a null value, or are preceded by an 'N'
- Calculate the Points without double points Friday
    - Rank the players based on this new field
    - Create a field to determine if there has been a change in winner for that particular Series 
      and Week
- Rank the players based on their Score instead
    - Create a field to determine if there has been a change in winner for that particular Series
      and Week
- Calculate the Score if the score on Friday was doubled (instead of the Points)
    - Rank the players based on this new field
    - Create a field to determine if there has been a change in winner for that particular Series 
      and Week
- Remove unnecessary fields
- Output the data

Author: Kelly Gilbert
Created: 2022-04-06
Requirements:
  - input dataset:
      - Richard Osman's House of Games - Episode Guide - Players.csv
  - output dataset (for results check only):
      - House of Games Output.csv
"""


import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input the dataset, rename fields, remove null and N Series
usecols=['Player', 'Ser.', 'Wk.', 'Week', 'Total', 'Week.1', 'F', 'F.1']
renames = {'Ser.' : 'Series', 'Wk.' : 'Week', 'Total' : 'Score', 'Week' : 'Points', 
           'Week.1' : 'Original_Rank', 'F.1' : 'F_rank'}

df = pd.read_csv(r".\inputs\Richard Osman's House of Games - Episode Guide - Players.csv",
                 usecols=usecols)\
       .rename(columns=renames)\
       .query("(Series.str[0] != 'N') and not (Series != Series)")\
       .assign(F=lambda df_x: df_x['F'].astype('int'),
               F_rank=lambda df_x: df_x['F_rank'].str[0].astype('int'),
               Original_Rank=lambda df_x: df_x['Original_Rank'].str[0].astype('int'))


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# calculate alternatives
df['Points_no_dpf'] = (df['Points'] - (5 - df['F_rank'])).astype(int)
df['Score_with_dpf'] = (df['Score'] + df['F']).astype(int)


# compare ranks based on points
group = df.groupby(['Series', 'Week'])

df['Rank without double points Friday'] = \
    group['Points_no_dpf'].rank('min', ascending=False).astype(int)
df['check1'] = ((df['Original_Rank'] == 1) & (df['Rank without double points Friday'] != 1))
df['Change in winner with no double points Friday?'] = group['check1'].transform('any')


# compare ranks based on score
df['Rank based on Score'] = group['Score'].rank('min', ascending=False).astype(int)
df['check2'] = ((df['Original_Rank'] == 1) & (df['Rank based on Score'] != 1))
df['Change in winner based on Score?'] = group['check2'].transform('any')


# compare ranks based on score (with Friday's score doubled)
df['Rank if Double Score Friday'] = group['Score_with_dpf'].rank('min', ascending=False).astype(int)
df['check3'] = ((df['Original_Rank'] == 1) & (df['Rank if Double Score Friday'] != 1))
df['Change in winner if Double Score Friday?'] = group['check3'].transform('any')
    

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.rename(columns={'Score_with_dpf' : 'Score if double Friday', 
                   'Points_no_dpf' : 'Points without double points Friday',
                   'Original_Rank' : 'Original Rank'})\
  .drop(columns=['F', 'F_rank', 'check1', 'check2', 'check3'])\
  .to_csv(r'.\outputs\output-2022-14.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['House of Games Output.csv']
my_files = ['output-2022-14.csv']
unique_cols = [['Series', 'Week', 'Player']]
col_order_matters = False
round_dec = 8

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
            print('\n\n*** Missing or extra records ***')
            print('\n\nIn solution, not in mine:\n')
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
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])
                                   & ((df_compare[f'{c}_sol'].notna()) 
                                      | (df_compare[f'{c}_mine'].notna()))]

            if len(unmatched) > 0:
                print(f'\n\n*** Values do not match: {c} ***\n')
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                errors += 1
        
        if errors == 0:
            print('Values match')

    print('\n')  

