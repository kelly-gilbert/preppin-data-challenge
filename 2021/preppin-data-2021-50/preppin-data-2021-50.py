# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 32- Excelling through Aggregation
https://preppindata.blogspot.com/2021/12/2021-week-50-departmental-december-sales.html

- Input the data
- Fill in the Salesperson names for each row (the name appears at the bottom of each monthly
  grouping)
- Bring out the YTD information from the October tracker and use it to create YTD totals for 
  November too
- Reshape the data so all the bike types are in a single column
- Output the data

Author: Kelly Gilbert
Created: 2021-08-15
Requirements:
  - input dataset:
      - Sales Department Input.xlsx
  - output dataset (for results check only):
      - Sales Department Output.csv
"""

from numpy import where
from pandas import concat, ExcelFile, melt, offsets, read_excel

# for results check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\inputs\Sales Department Input.xlsx') as xl:
    df = concat([read_excel(xl, s).assign(sheet=s) for s in xl.sheet_names])\
         .rename(columns={'Unnamed: 7' : 'YTD Total'})


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# get the month (for total rows, use the date from the prior row) -- use for YTD calc
df['Month'] = where(df['Salesperson'].notna(), 
                   df['Date'].shift(1) - offsets.MonthBegin(1, normalize=True),
                   df['Date']).astype('datetime64[M]')
df['Year'] = df['Month'].dt.year


# fill in the Salesperson names for each row
df['Salesperson'] = df['Salesperson'].fillna(method='bfill')


# reshape the data so all the bike types are in a single column
df_m = df[df['Date'].notna()].drop(columns=['RowID', 'Total', 'YTD Total', 'sheet'])\
         .melt(id_vars=['Salesperson', 'Date', 'Month', 'Year'], 
               var_name='Bike Type', value_name='Sales')


# get the monthly totals by salesperson, and merge to get the YTD values for the first month
df_tot = df_m.groupby(['Month', 'Year', 'Salesperson'])['Sales'].sum().reset_index()\
         .merge(df[df['YTD Total'].notna()][['Month', 'Salesperson', 'YTD Total']],
                how='outer', on=['Month', 'Salesperson'])\
         .sort_values(by=['Salesperson', 'Month'])
         

# get the cumulative sum of the YTD total + future months
df_tot['YTD Total2'] = where(df_tot['YTD Total'].isnull(), df_tot['Sales'], df_tot['YTD Total'])
df_tot['YTD Total'] = df_tot.groupby(['Salesperson', 'Year'])['YTD Total2'].cumsum()
df_tot.drop(columns=['Sales', 'YTD Total2'], inplace=True)
    

# add YTD total to main data
df_m = df_m.merge(df_tot, how='left', on=['Month', 'Salesperson'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

cols = ['Salesperson', 'Date', 'Bike Type', 'Sales', 'YTD Total']
df_m.to_csv(r'.\outputs\output-2021-50.csv', index=False, columns=cols, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Sales Department Output.csv']
my_files = ['output-2021-50.csv']
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
