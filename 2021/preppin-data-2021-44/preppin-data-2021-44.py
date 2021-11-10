# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 44 - On yer bike!
https://preppindata.blogspot.com/2021/11/2021-week-44-on-yer-bike.html

- Input the data
- Convert the Value field to just be Kilometres ridden 
    - Carl cycles at an average of 30 kilometres per hour whenever he is measuring his sessions 
      in minutes
- Create a field called measure to convert KM measurements into 'Outdoors' and any measurement in 
  'mins' as 'Turbo Trainer'.
- Create a separate column for Outdoors and Turbo Trainer (indoor static bike values)
- Ensure there is a row for each date between 1st Jan 2021 and 1st Nov 2021(inclusive)
- Count the number of activities per day and work out the total distance cycled Outdoors or on the 
  Turbo Trainer
- Change any null values to zero
- Work out how many days I did no activities
- Output a file to help me explore the analysis further


Author: Kelly Gilbert
Created: 2021-11-08
Requirements:
  - input dataset:
      - Carl's 2021 cycling.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 44 Output.csv
"""


from numpy import where
from pandas import date_range, ExcelFile, pivot_table, read_excel

# for results check only
from pandas import read_csv

#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r".\inputs\Carl's 2021 cycling.xlsx") as xl:
    df = read_excel(xl)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# convert the Value field to just be Kilometres ridden (assuming 30 km/hr)
df['km'] = where(df['Measure'].str.lower() == 'min', df['Value'] * 30 / 60, df['Value'])    
    
# classify as 'Outdoors' if measure is km, and 'Turbo Trainer' otherwise
df['type'] = where(df['Measure'].str.lower() == 'km', 'Outdoors', 'Turbo Trainer')  
  
# create a separate column for Outdoors and Turbo Trainer (indoor static bike values)
df_p = df.pivot_table(values='km', index='Date', columns='type', aggfunc='sum')

# count the number of activities per day
df_p['Activities per day'] = df.groupby('Date')['km'].count().astype('Int64')

# ensure there is a row for each date between 1st Jan 2021 and 1st Nov 2021(inclusive)
rng = date_range(start='2021-01-01', end='2021-11-01')
df_p = df_p.reindex(rng).fillna(0).rename_axis('Date').reset_index()


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# work out how many days I did no activities
print(f'Days with no activities: {df_p[df_p["Activities per day"] == 0]["Date"].count()}')


df_p.to_csv(r'.\outputs\output-2021-44.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 44 Output.csv']
my_files = ['output-2021-44.csv']
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


df_solution[df_solution['Date']=='22/10/2021']
df_mine[df_mine['Date']=='22/10/2021']

df[df['Date']=='2021-10-22']

df['km'].sum()
df_solution['Outdoors'].sum() + df_solution['Turbo Trainer'].sum()
df_mine['Outdoors'].sum() + df_mine['Turbo Trainer'].sum()
