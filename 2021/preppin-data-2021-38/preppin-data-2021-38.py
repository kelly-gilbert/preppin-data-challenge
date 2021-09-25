# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 38 - Trilogy
https://preppindata.blogspot.com/2021/09/2021-week-38-trilogy.html

- Input the data
- Split out the Number in Series field into Film Order and Total Films in Series
- Work out the average rating for each trilogy
- Work out the highest ranking for each trilogy
- Rank the trilogies based on the average rating and use the highest ranking metric to break ties
  (make sure you haven't rounded the numeric fields yet!)
- Remove the word trilogy from the Trilogy field
- Bring the 2 datasets together by the ranking fields
- Output the data

Author: Kelly Gilbert
Created: 2021-08-15
Requirements:
  - input dataset:
      - Trilogies Input.xlsx
  - output dataset (for results check only):
      - Trilogies Output.csv
"""


from pandas import merge, ExcelFile, read_excel

# for results check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Trilogies Input.xlsx') as xl:
    df_t = read_excel(xl, 'Top 30 Trilogies')
    df_f = read_excel(xl, 'Films')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split out the Number in Series field into Film Order and Total Films in Series
df_f[['Film Order', 'Total Films in Series']] = df_f['Number in Series'].str.extract('(.*)/(.*)')


# avg, max for each trilogy
# rank the trilogies based on the average rating and use the highest ranking metric to break ties
df_sum = df_f.groupby('Trilogy Grouping').agg(Trilogy_Average=('Rating', 'mean'),
                                              Trilogy_Max=('Rating', 'max'))\
             .sort_values(['Trilogy_Average', 'Trilogy_Max'], ascending=False)\
             .reset_index()
df_sum.columns = [c.replace('_', ' ') for c in df_sum.columns]
df_sum['Trilogy Ranking'] = df_sum.index + 1


# remove the word trilogy from the Trilogy field
df_t['Trilogy'] = df_t['Trilogy'].str.replace(' trilogy', '')


# bring the 2 datasets together by the ranking fields
df = df_sum.merge(df_t, on='Trilogy Ranking')\
           .merge(df_f, on='Trilogy Grouping')
df['Trilogy Average'] = df['Trilogy Average'].round(1)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

columns = ['Trilogy Ranking', 'Trilogy', 'Trilogy Average', 'Film Order', 'Title', 'Rating',
           'Total Films in Series']
df.to_csv(r'.\outputs\output-2021-38.csv', index=False, columns=columns)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Trilogies Output.csv']
my_files = ['output-2021-38.csv']
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
