# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 10 - Pokémon Hierarchies
https://preppindata.blogspot.com/2021/02/2021-week-10-pokemon-hierarchies.html

- Input the data
- Our Pokémon dataset actually contains too many Pokémon: 
    - We're only interested in Pokémon up to Generation III, which is up to (and including) 
      number 386
- This means we're also not interested in mega evolutions so we can filter Pokémon whose name start 
  with "Mega"
- Some Pokémon have more than one Type. We aren't interested in Types for this challenge so remove 
- this field and ensure we have one row per Pokémon
- Now we want to bring in information about what our Pokémon evolve to
- Warning!  In our Evolution dataset, we still have Pokémon beyond Gen III. You'll need to filter 
  these out too, from both the evolved from and evolved to fields
- Bring in information about what a Pokémon evolves from
- Ensure that we have all 386 of our Pokémon, with nulls if they don't have a pre-evolved form or 
  if they don't evolve
- Finally, for Pokémon that have 3 evolutions, we want to know what the First Evolution is in their 
  Evolution Group
- Some duplication may have occurred with all our joins, ensure no 2 rows are exactly the same
- Create a calculation for our Evolution Group
- The Evolution Group will be named after the First Evolution e.g. in the above example, Bulbasaur 
  is the name of the Evolution Group
- Output the data

Author: Kelly Gilbert
Created: 2021-03-19
Requirements:
  - input dataset:
      - Pokemon Input.xlsx
  - output dataset (for results check):
      - Pokemon Output.csv

"""

from pandas import ExcelFile, read_excel
from numpy import nan

# used for answer check only
from pandas import read_csv


def get_evolution_group(p_name):
    """
    given a Pokemon name, returns the first Pokemon in the evolution hierarchy
    
    e_dict = a dictionary of evolution steps (keys: evolving to, values: evolving from)
    p_name = the Pokemon name to look up
    """
    if p_name not in evolution_dict.keys() or p_name == evolution_dict[p_name]: 
        return p_name
    else:
        return get_evolution_group(evolution_dict[p_name])
    

#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Pokemon Input.xlsx') as xl:
    pokemon = read_excel(xl, 'Pokemon')
    evolution = read_excel(xl, 'Evolution')


#---------------------------------------------------------------------------------------------------
# filter the pokemon and evolution lists
#---------------------------------------------------------------------------------------------------

# keep up to Generation III (up to and including #386) and not Mega evolutions
pokemon = pokemon[(pokemon['#'].astype(float) <= 386) & (pokemon['Name'].str.slice(0,5) != 'Mega ')]

# remove multiple rows for different types 
pokemon.drop(columns=['Type'], inplace=True)
pokemon.drop_duplicates(inplace=True)

# remove non-gen III from the evolution dataset
valid_names = list(pokemon['Name'])
evolution = evolution[(evolution['Evolving from'].isin(valid_names)) &
                      (evolution['Evolving to'].isin(valid_names))]


#---------------------------------------------------------------------------------------------------
# get evolution info
#---------------------------------------------------------------------------------------------------

evolution_dict = dict(zip(evolution['Evolving to'], evolution['Evolving from']))

# bring in information about what our Pokémon evolve TO (keep nulls)
df = pokemon.merge(evolution, left_on='Name', right_on='Evolving from', how='left')

# bring in information about what a Pokémon evolves FROM (keep nulls)
df['Evolving from'] = [evolution_dict[k] if k in evolution_dict.keys() else nan for k in df['Name']]

# get the first Pokemon in the evolution hierarchy
df['Evolution Group'] = df['Name'].apply(get_evolution_group)

# if it is a 3rd+ evolution, add the first evolution
df['First Evolution'] = [nan if (n==g) | (g==f) else g 
                         for n,g,f in zip(df['Name'], df['Evolution Group'], df['Evolving from'])]

# ensure we still have all of the Pokemon
if not pokemon['Name'].unique().sort() == df['Name'].unique().sort():
    print('The list of Pokemon does not match after joins')
    raise SystemExit
    
# ensure all rows are unique
df.drop_duplicates(inplace=True)


# --------------------------------------------------------------------------------------------------
# output the data
# --------------------------------------------------------------------------------------------------

output_cols = ['Evolution Group'] + list(pokemon.columns) + list(evolution.columns) + \
              ['First Evolution']
df.to_csv('.\\outputs\\output-2021-10.csv', index=False, columns=output_cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solutionFiles = ['Pokemon Output.csv']
myFiles = ['output-2021-10.csv']
col_order_matters = False


for i in range(len(solutionFiles)):
    print('\n---------- Checking \'' + myFiles[i] + '\' ----------\n')

    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solutionFiles[i])
    dfMine = read_csv('.\\outputs\\' + myFiles[i])

    # are the fields the same and in the same order?
    solutionCols = list(dfSolution.columns)
    myCols = list(dfMine.columns)
    if not col_order_matters:
        solutionCols.sort()
        myCols.sort()

    col_match = False
    if solutionCols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(dfSolution.columns)))
        print('    Columns in mine    : ' + str(list(dfMine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        dfSolution['join'] = 1
        dfMine['join'] = 1
        dfCompare = dfSolution.merge(dfMine, how='outer', on=list(dfSolution.columns)[:-1])
        dfCompare.rename(columns={'join_x':'in_solution', 'join_y':'in_mine'}, inplace=True)

        if len(dfCompare[dfCompare['in_solution'].isna() | dfCompare['in_mine'].isna()]) > 0:
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')

    print('\n')
