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
    - Create a field to determine if there has been a change in winner for that particular Series and Week
- Rank the players based on their Score instead
    - Create a field to determine if there has been a change in winner for that particular Series and Week
- Calculate the Score if the score on Friday was doubled (instead of the Points)
    - Rank the players based on this new field
    - Create a field to determine if there has been a change in winner for that particular Series and Week
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


from numpy import where
import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input the dataset, rename fields, remove null and N* Series
df_input = pd.read_csv(r".\inputs\Richard Osman's House of Games - Episode Guide - Players.csv")\
             .rename(columns={'Ser.' : 'Series', 
                              'Wk.' : 'Week', 
                              'T' : 'Tu', 
                              'T.1' : 'Th', 
                              'Total' : 'Score', 
                              'Week' : 'Points', 
                              'Week 1' : 'Rank'})\
            .query("(Series.str[0] != 'N') and not (Series != Series)")\
            .melt(id_vars=['Series', 'Week', 'Player'], value_vars=['M','Tu','W','Th', 'F'], 
                  var_name='day', value_name='score')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# calculate the points with and witout double points Friday
df_input['points'] = df_input.groupby(['Series', 'Week', 'day'])['score'].rank('max')
df_input['points_dpf'] = df_input['points'] * where(df_input['day'] == 'F', 2, 1)
df_input['score_dpf'] = df_input['score'] * where(df_input['day'] == 'F', 2, 1)


# summarize by series/week/player
df = df_input.groupby(['Series', 'Week', 'Player'], as_index=False)\
             [['points', 'points_dpf', 'score', 'score_dpf']].sum()


# points
group = df.groupby(['Series', 'Week'])
df['Original Rank'] = group['points_dpf'].rank(method='min', ascending=False)
df['Rank without double points Friday'] = group['points'].rank('min', ascending=False)
df['Change in winner with no double points Friday?'] = \
    (group['Original Rank'].idxmin() != group['Rank without double points Friday'].idxmin())


# score
df['Rank based on Score'] = df.groupby(['Series', 'Week'])['score'].rank('min', ascending=False)
df['Change in winner based on Score?'] = \
    (df['Rank without double points Friday'] != df['Rank based on Score'])
    
df['Rank if Double Score Friday'] = df.groupby(['Series', 'Week'])['score_dpf'].rank('min', ascending=False)
df['Change in winner if Double Score Friday?]
  
    
    
Original Rank

df.groupby(['Series', 'Week'])['Original Rank'].idxmin().iloc[0:20]

df[(df['Series']=='2') & (df['Week']==3)][['Player', 'points', 'points_dpf', 'score', 'Original Rank']]




    - Rank the players based on this new field
    - Create a field to determine if there has been a change in winner for that particular Series and Week
- Rank the players based on their Score instead
    - Create a field to determine if there has been a change in winner for that particular Series and Week
- Calculate the Score if the score on Friday was doubled (instead of the Points)
    - Rank the players based on this new field
    - Create a field to determine if there has been a change in winner for that particular Series and Week
- Remove unnecessary fields
- Output the data









#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-14.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['House of Games Output.csv']
my_files = ['output-2022-14.csv']
unique_cols = ['Month']
col_order_matters = True
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
