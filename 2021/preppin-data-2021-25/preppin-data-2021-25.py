# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 25 - The Worst Pokemon
https://preppindata.blogspot.com/2021/06/2021-week-25-worst-pokemon.html

- Input the data
- Clean up the list of Gen 1 Pokémon so we have 1 row per Pokémon
- Clean up the Evolution Group input so that we can join it to the Gen 1 list 
    - Filter out Starter and Legendary Pokémon
- Using the Evolutions input, exclude any Pokémon that evolves from a Pokémon that is not part of
  Gen 1 or can evolve into a Pokémon outside of Gen 1
- Exclude any Pokémon with a mega evolution, Alolan, Galarian or Gigantamax form
- It's not possible to catch certain Pokémon in the most recent games. These are the only ones we
  will consider from this point on
- We're left with 10 evolution groups. Rank them in ascending order of how many times they've
  appeared in the anime to see who the worst Pokémon is!
- Output the data

Author: Kelly Gilbert
Created: 2021-06-23
Requirements:
  - input dataset:
      - 2021W25 Input.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 24 Output.csv
"""


from pandas import concat, ExcelFile, merge, read_excel


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\2021W25 Input.xlsx') as xl:
    gen1 = read_excel(xl, 'Gen 1')
    evol_group = read_excel(xl, 'Evolution Group')
    evol = read_excel(xl, 'Evolutions')
    exclude = concat([read_excel(xl, s) for s in ['Mega Evolutions', 'Alolan', 'Galarian', 
                                                  'Gigantamax']])
    unattainable = read_excel(xl, 'Unattainable in Sword & Shield')
    appearances = read_excel(xl, 'Anime Appearances').drop_duplicates()


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# clean up the list of Gen 1 Pokémon so we have 1 row per Pokémon
# the type (which wraps to the next row) is not used
gen1 = gen1.loc[gen1['#'].notna()]

# clean the evolution group #
evol_group['#'] = evol_group['#'].astype(int)
evol_group.drop_duplicates(subset=['#', 'Evolution Group'], inplace=True)

# get the evolution group for gen1
gen1 = gen1[['#', 'Name']].merge(evol_group, on='#', how='inner')


# get the to/from evolutions for gen1
evol.drop(columns=['Evolution Type', 'Condition', 'Level'], inplace=True)
gen1 = gen1.merge(evol, left_on='Name', right_on='Evolving to', how='left')\
           .drop(columns=['Evolving to'])
gen1 = gen1.merge(evol, left_on='Name', right_on='Evolving from', suffixes=['', '_r'], how='left')\
           .drop(columns=['Evolving from_r'])


# get the list of Pokemon with a mega evolution, Alolan, Galarian or Gigantamax form
exclude['Name_clean'] = exclude['Name'].str.extract('(?:\w+) (.*?)(?: [XY]|$)')
exclude_list = exclude.merge(gen1[['Name', 'Evolution Group']], left_on='Name_clean', 
                             right_on='Name', how='inner')['Evolution Group'].unique()


# get the final list:
#    - is in unattainable list
#    - not starter or legendary
#    - does not evolve from/to a non-gen1 pokemon
#    - does not have gigantamax, etc., form
df = gen1.loc[gen1['Evolution Group'].isin(unattainable['Name'])
              & (gen1['Starter?'] != 1) 
              & (gen1['Legendary?'] != 1)
              & (gen1['Evolving from'].isna() | gen1['Evolving from'].isin(gen1['Name']))
              & (gen1['Evolving to'].isna() | gen1['Evolving to'].isin(gen1['Name']))
              & ~gen1['Evolution Group'].isin(exclude_list)]\
         .groupby('Evolution Group').size().reset_index().drop(columns=[0])


# summarize the appearances by Evolution Group
appear_x_eg = appearances.merge(gen1[['Name', 'Evolution Group']], left_on='Pokemon', 
                                right_on='Name', how='inner')\
                         .groupby('Evolution Group').agg(Appearances=('Episode', 'nunique'))\
                         .reset_index()


# get the appearances for each evolution group of interest
df = df.merge(appear_x_eg, on='Evolution Group').sort_values(by='Appearances')


# rank the groups by appearances
df['The Worst Pokémon'] = df['Appearances'].rank(method='min').astype(int)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2021-25.csv', index=False, 
          columns=['The Worst Pokémon', 'Evolution Group', 'Appearances'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week