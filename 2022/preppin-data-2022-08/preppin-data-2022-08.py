# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 8 - Pokémon Evolution Stats
https://preppindata.blogspot.com/2022/02/2022-week-8-pokemon-evolution-stats.html

- Import the data (excel file)
- From pkmn_stats dataset remove the columns height, weight and evolves from
- Pivot (wide to long) pkmn stats so that hp, attack, defense, special_attack, special_defense, and
  speed become a column called 'combat_factors'
- Using the evolutions data look up the combat_factors for each Pokémon at each stage, making sure 
  that the combat_factors match across the row, i.e. we should be able to see the hp for Bulbasaur, 
  Ivysaur and Venusaur on one row
- Remove any columns for 'pokedex_number' and 'gen_introduced' that were from joins at Stage 2 & 3
- If a Pokémon doesn't evolve remove it from the dataset
- Find the combat power values relating to the Pokémon's last evolution stage
- Sum together each Pokémon's combat_factors
- Find the percentage increase in combat power from the first & last evolution stage
- Sort the dataset, ascending by percentage increase
- If using Tableau Prep, consider introducing a field to manage this sort and then hide it
- Output the data
- Which Pokémon stats decrease from evolving?

Author: Kelly Gilbert
Created: 2022-02-24
Requirements:
  - input dataset:
      - input_pkmn_stats_and_evolutions.xlsx
  - output dataset (for results check only):
      - output_preppin_data_gnv_feb.csv
"""


from numpy import where
import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

drop_cols = ['weight', 'height', 'evolves_from']

with pd.ExcelFile(r'.\inputs\input_pkmn_stats_and_evolutions.xlsx') as xl:
  
    # read in the stats tab, pivot combat factors to rows, then sum the combat factors
    df_stat = pd.read_excel(xl, 'pkmn_stats', usecols=lambda c: c not in drop_cols)\
                .melt(id_vars=['name', 'pokedex_number', 'gen_introduced'])\
                .groupby(['name', 'pokedex_number', 'gen_introduced'], as_index=False)[['value']].sum()
    
    # read in the evolutions tab, keep records that have at least one evolution           
    df_evol = pd.read_excel(xl, 'pkmn_evolutions')\
                .query('Stage_2==Stage_2 or Stage_3==Stage_3')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# find the inital and final combat power
df_evol['final_evol'] = where(df_evol['Stage_3'].isna(), df_evol['Stage_2'], df_evol['Stage_3'])

df_out = df_evol.merge(df_stat, left_on='Stage_1', right_on='name', how='left')\
                .drop(columns=['name'])\
                .merge(df_stat[['name', 'value']], left_on='final_evol', right_on='name', how='left')\
                .drop(columns=['name'])\
                .rename(columns={'value_x' : 'initial_combat_power', 'value_y' : 'final_combat_power'})

df_out['combat_power_increase'] = df_out['final_combat_power'] / df_out['initial_combat_power'] - 1


#---------------------------------------------------------------------------------------------------
# question: Which Pokémon stats decrease from evolving?
#---------------------------------------------------------------------------------------------------

print('Which Pokémon stats decrease from evolving?')
print(df_out[df_out['combat_power_increase'] < 0].iloc[0]['Stage_1'])
print('\n' * 2)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.drop(columns=['final_evol'])\
      .to_csv(r'.\outputs\output-2022-08.csv', index=False, encoding='utf-8')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['output_preppin_data_gnv_feb.csv']
my_files = ['output-2022-08.csv']
unique_cols = [['Stage_1', 'Stage_2', 'Stage_3']]
col_order_matters = True
round_dec = 8

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_sol = pd.read_csv('.\\outputs\\' + solution_file, encoding='ISO-8859-1')
    df_mine = pd.read_csv('.\\outputs\\' + my_files[i], encoding='utf-8')

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
