# -*- coding: utf-8 -*-
"""
Preppin' Data 2019: Week 4
https://preppindata.blogspot.com/2019/03/2019-week-4.html

- Import the file
- Fix some date issues!
- Split the "Hi-" categories up so player and value is separate
- Determine whether each game was played by the Spurs: Home or Away
- Determine whether the Spurs won or lost each game
- Get rid of unrequired columns
- Output: (this is less prescribed this week)
  - 64 rows of data (excluding the headers)
  - 13 columns (you might have different)
  - One row per game
  - No cells without a value


Author: Kelly Gilbert
Created: 2021-08-20
Requirements:
  - input dataset:
      - PD - ESPN stats.xlsx
  - output dataset (for results check only):
      - Week Four Output.csv
"""


from numpy import where
from pandas import DateOffset, ExcelFile, read_excel

# for results check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\PD - ESPN stats.xlsx') as xl:
    df = read_excel(xl, 'Sheet1', converters={'W-L' : str})


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# fix date: year for Oct-Dec dates should be 2018 instead of 2019
df['True Date'] = where(df['DATE'].dt.month > 6, df['DATE'] - DateOffset(years=1), df['DATE'])


# split the "Hi-" categories up so player and value is separate
for c in [c for c in df.columns if c.startswith('HI ')]:
    df[[f'{c} - Player', f'{c} - Value']] = df[f'{c}'].str.extract('(.*?) (\d+)')


# determine whether each game was played by the Spurs: Home or Away
df['Home or Away'] = where(df['OPPONENT'].str.match('^vs'), 'Home', 'Away')
df['Opponent (clean)'] = df['OPPONENT'].str.extract('(?:vs|\@)(.+)')


# determine whether the Spurs won or lost each game
df['Win or Loss'] = df['RESULT'].str[0]


# fix win-loss that imported as date
df['W-L'] = df['W-L'].str.replace('\d{4}-0?(\d+)-0?(\d+).*', lambda x: f'{x.group(2)}-{x.group(1)}')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Opponent (clean)', 'HI ASSISTS - Player', 'HI ASSISTS - Value', 'HI REBOUNDS - Player',
            'HI REBOUNDS - Value', 'HI POINTS - Player', 'HI POINTS - Value', 'Win or Loss',
            'Home or Away', 'True Date', 'OPPONENT', 'RESULT', 'W-L']
df.to_csv(r'.\outputs\output-2019-04.csv', index=False, columns=out_cols, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Week Four Output.csv']
my_files = ['output-2019-04.csv']
col_order_matters = True

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_file)
    df_mine = read_csv('.\\outputs\\' + my_files[i])

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
