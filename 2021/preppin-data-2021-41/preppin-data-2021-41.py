# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 41 - Southend Stats
https://preppindata.blogspot.com/2021/10/2021-week-41-southend-stats.html

- Input the data
- Rename the penultimate column from P 1 (as it appears in Prep) to Pts
- Exclude null rows
- Create a Special Circumstances field with the following categories
    - Incomplete (for the most recent season) 
    - Abandoned due to WW2 (for the 1939 season)
    - N/A for full seasons
- Ensure the POS field only has values for full seasons
- Extract the numeric values from the leagues
    - FL-CH should be assigned a value of 0 
    - NAT-P should be assigned a value of 5
- Create an Outcome field with 3 potential values. (Note: this should apply to all seasons in the 
  data order regardless of any gaps. The current season will have a null value)
    - Promoted, where they are in a league higher than their current league in the following season
    - Relegated, where they are in a league lower than their current league in the following season
    - Same League, where they do not change leagues between seasons
- Create new rows for seasons that were missed due to WW1 and WW2
- Update the fields with relevant values for these new rows
  e.g. change their Special Circumstances value to WW1/WW2
- Output the data

Author: Kelly Gilbert
Created: 2021-10-14
Requirements:
  - input dataset:
      - Southend Stats.csv
  - output dataset (for results check only):
      - 2021W41 Output.csv
"""


from numpy import nan, where
from pandas import DataFrame, read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\\inputs\\Southend Stats.csv', sep='\s+').rename(columns={'P.1' : 'Pts'})
df.columns = [c if c == 'POS' else c.title() for c in df.columns]


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create a Special Circumstances field with the following categories
df['Special Circumstances'] = where(df['Season'] == df['Season'].max(), 'Incomplete',
                                where(df['Season'] == '1939-40', 'Abandoned due to WW2', 'N/A'))

# ensure the POS field only has values for full seasons
df['POS'] = where(df['Special Circumstances'] == 'N/A', df['POS'], nan)

# extract the numeric values from the leagues
df['league_nbr'] = where(df['League'] == 'FL-CH', 0,
                     where(df['League'] == 'NAT-P', 5,
                           df['League'].str.extract('.*-(\d+)', expand=False).astype(float)))

# create an Outcome field with 3 potential values. (Note: this should apply to all seasons in the
# data order regardless of any gaps. The current season will have a null value)
df = df.sort_values(by='Season')
df['Outcome'] = where(df['league_nbr'].shift(-1) < df['league_nbr'], 'Promoted',
                  where(df['league_nbr'].shift(-1) > df['league_nbr'], 'Relegated',
                    where(df['league_nbr'].shift(-1) == df['league_nbr'], 'Same League', 'N/A')))


# create new rows for seasons that were missed due to WW1 and WW2
missing_years = [*range(1915, 1919), *range(1940, 1946)]
df_adds = DataFrame({'Season' : [f'{y}-{(y+1) % 100}' for y in missing_years],
                     'Special Circumstances' : ['WW1' if y <= 1919 else 'WW2' for y in missing_years],
                     'Outcome' : ['N/A']*len(missing_years)})
df = df.append(df_adds)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2021-41.csv', index=False, float_format='%d',
          columns=['Season', 'Outcome', 'Special Circumstances', 'League', 'P', 'W', 'D', 'L',
                   'F', 'A', 'Pts', 'POS'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['2021W41 Output.csv']
my_files = ['output-2021-41.csv']
col_order_matters = True

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_file, keep_default_na=False)
    df_mine = read_csv('.\\outputs\\' + my_files[i], keep_default_na=False)

    # are the fields the same and in the same order?
    solution_cols = list(df_solution.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_solution.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        # round float values
        s = df_solution.dtypes.astype(str)
        for c in s[s.str.contains('float')].index:
            df_solution[c] = df_solution[c].round(8)
            df_mine[c] = df_mine[c].round(8)

        # join the dataframes on all columns except the in flags
        df_solution_compare = df_solution.merge(df_mine, how='outer',
                                                on=list(df_solution.columns),
                                                suffixes=['_solution', '_mine'], indicator=True)

        if len(df_solution_compare[df_solution_compare['_merge'] != 'both']) > 0:
            print('*** Values do not match ***\n')
            print('In solution, not in mine:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'left_only']) 
            print('\n\n')
            print('In mine, not in solution:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'right_only']) 
            
        else:
            print('Values match')

    print('\n')
