# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 31- Excelling in Prep
https://preppindata.blogspot.com/2021/08/2021-week-36-excelling-in-prep.html

- Input data
- Remove the 'Return to Manufacturer' records
- Create a total for each Store of all the items sold (help)
- Aggregate the data to Store sales by Item
- Output the data

Author: Kelly Gilbert
Created: 2021-08-15
Requirements:
  - input dataset:
      - PD 2021 Wk 31 Input.csv
  - output dataset (for results check only):
      - PD 2021 Wk 31 Output.csv
"""


from pandas import pivot_table, read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\\inputs\\PD 2021 Wk 31 Input.csv', parse_dates=['Date'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# remove the 'Return to Manufacturer' records
df = df.loc[df['Status'] != 'Return to Manufacturer']

# pivot the data by store and item
total_name = 'Items sold per store'
pivot = pivot_table(df, values='Number of Items', index='Store', columns='Item', aggfunc='sum', 
                    fill_value=None, margins=True, margins_name=total_name)\
                   .reset_index()


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

cols = list(pivot.columns)
cols.reverse()

pivot.iloc[0:len(pivot)-1].to_csv(r'.\outputs\output-2021-31.csv', index=False, columns=cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 31 Output.csv']
my_files = ['output-2021-31.csv']
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
