# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 48 Departmental December - Finance
https://preppindata.blogspot.com/2021/12/2021-week-48-departmental-december.html

- Input the data
- Extract each data table within the Excel workbook
- Extract the branch name from the table structure
- Create a row per measure and year
- Remove the word 'Year' from the year values
- Create a True Value (i.e. the correct number of zeros for the measure)
- Remove the suffix of the measure (i.e. the (k) or (m) if the measure name has the units)
- Remove unneeded columns
- Output the data

Author: Kelly Gilbert
Created: 2021-12-01
Requirements:
  - input dataset:
      - PD 2021 Wk 48 Input.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 48 Output.csv
"""


from numpy import nan, where
from pandas import ExcelFile, melt, read_excel, Series

# for results check only:
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# import the sheet and remove any cols or rows that are totally blank
with ExcelFile(r'.\\inputs\\PD 2021 Wk 48 Input.xlsx') as xl:
    df = read_excel(xl).dropna(axis=1, how='all').dropna(axis=0, how='all').reset_index(drop=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# melt values into rows       
df_melt = df.melt(id_vars=['Unnamed: 1'],
                  value_vars=[c for c in df.columns if c != 'Unnamed: 1'],
                  value_name='True Value')\
            .dropna(subset=['True Value'])\
            .reset_index(drop=True)

# copy down the branch name
df_melt['Branch'] = Series(where(df_melt['True Value'].str.contains('Year')==True,
                                 df_melt['Unnamed: 1'], nan))\
                    .fillna(method='ffill')

# copy down the year
df_melt['Recorded Year'] = Series(where(df_melt['True Value'].str.contains('Year')==True,
                                        df_melt['True Value'].str.replace('Year ', ''), nan))\
                           .fillna(method='ffill')\
                           .astype(int)

# clean the measure names and update the True Values based on the unit
multiplier = { '(k)' : 1000, '(m)' : 1000000 }
df_melt = df_melt.loc[df_melt['True Value'].str.contains('Year ').isna()]
df_melt[['Clean Measure names', 'unit']] = df_melt['Unnamed: 1'].str.extract('(.*?) ?(\(.*\))?$')
df_melt['True Value'] = df_melt['True Value'] * df_melt['unit'].replace(multiplier).fillna(1)

# drop extra columns
df_melt.drop(columns=['Unnamed: 1', 'unit', 'variable'], inplace=True)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_melt.to_csv(r'.\outputs\output-2021-48.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 48 Output.csv']
my_files = ['output-2021-48.csv']
col_order_matters = False

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
