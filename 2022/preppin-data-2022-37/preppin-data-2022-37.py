# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 37 - Elden Ring Adventure
https://preppindata.blogspot.com/2022/09/2022-week-37-elden-ring-adventure.html

- Load the dataset - updated 14/09
- Split the dataset into two tables
  - Damage Stats: 1 containing: Name, Category, Phy, Mag, Fire, Ligh, Holy
  - Level Requirements: 1 containing: Name, Str, Dex, Int, Fai, Arc
- For Damage Stats, if you look at the data in Phy, Mag, Fire, Ligh, Holy:
  - the first value shows the attack damage 
  - the second value shows the damage resistance
  - A dash “-” means 0, i.e. no damage 
- For Level Requirements, for Str, Dex, Int, Fai, Arc:
  - the first value shows the level required
  - the second value shows the weapon scaling rating
  - A dash “-” means 0, i.e. no requirement or scaling 
- Pivot the two datasets:
  - For Damage Stats,1 column containing Phy, Mag, Fire, Ligh, Holy and 1 for the values
  - For Level Requirements,1 column containing Str, Dex, Int, Fai, Arc and 1 for the values
- Split the pivot values into 2 columns for both tables:
  - For Damage Stats label the first column “Attack Damage”, and the second “Damage Resistance”
  - For Level Requirements label the first column “Required Level”, and the second “Attribute Scaling” 
- Replace the “-” values with zero in the columns: “Attack Damage”, “Damage Resistance”, “Required Level” and change the datatype to whole numbers (integer)
- Find the total “Attack Damage” and total “Required Level” for all weapons and join the datasets together.
- Rank the weapons by total attack damage, grouped by the total required attribute. 
- Filter for the number 1 rank and output the data

Author: Kelly Gilbert
Created: 2022-09-19
Requirements:
  - input dataset:
      - elden_ring_combat_weapons_raw.csv
  - output dataset (for results check only):
      - Best Damage Per Level.csv
"""


from numpy import where
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

ID_COLS = ['Name', 'Category']
DAMAGE_COLS = ['Phy', 'Mag', 'Fire', 'Ligh', 'Holy']
LEVEL_COLS = ['Str', 'Dex', 'Int', 'Fai', 'Arc']

DAMAGE_RENAMES = {'val1' : 'Attack Damage', 'val2' : 'Damage Resistance' }
LEVEL_RENAMES = {'val1' : 'Required Level', 'val2' : 'Attribute Scaling' }


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input the file and melt the subset of columns into rows
df = ( pd.read_csv(r'.\inputs\elden_ring_combat_weapons_raw.csv', 
                   usecols=ID_COLS + DAMAGE_COLS + LEVEL_COLS)
         .melt(id_vars=ID_COLS, var_name='orig_col', value_name='orig_value')
     )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split the two values into separate columns and replace non-numeric values with zero
df[['val1', 'val2']] = ( df['orig_value'].str.replace('[^\s\d]', '0', regex=True)
                                         .str.extract('(\S*) (\S*)')
                                         .astype(int) )


# melt the two values into rows, calculate the new column name, pivot to new cols
df2 = ( df.melt(id_vars=ID_COLS + ['orig_col'], value_vars=['val1', 'val2'], var_name='value_type')
          .assign(new_col_name = lambda df_x: where(df_x['orig_col'].isin(DAMAGE_COLS), 
                                                    df_x['value_type'].replace(DAMAGE_RENAMES),
                                                    df_x['value_type'].replace(LEVEL_RENAMES)))
          .pivot_table(index=ID_COLS, columns='new_col_name', values='value', aggfunc='sum')
          .reset_index() )


# rank by attack damage, within required attribute
df2['Rank'] = df2.groupby('Required Level')['Attack Damage'].rank(ascending=False, method='min')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# output the top-ranked item for each level
( df2[df2['Rank']==1][['Name', 'Category', 'Required Level', 'Attack Damage']]
      .to_csv(r'.\outputs\output-2022-37.csv', index=False) )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Best Damage Per Level.csv']
my_files = [r'.\outputs\output-2022-37.csv']
unique_cols = [['Name', 'Category', 'Required Level']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
