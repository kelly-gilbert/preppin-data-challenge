# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 26 - Rolling Weekly Revenue
https://preppindata.blogspot.com/2021/06/2021-week-26-rolling-weekly-revenue.html

- Input data
- Create a data set that gives 7 rows per date (unless those dates aren't included in the data set). 
  ie 1st Jan only has 4 rows of data (1st, 2nd, 3rd & 4th)
- Remove any additional fields you don't need 
- Create the Rolling Week Total and Rolling Week Average per destination
- Records that have less than 7 days data should remain included in the output
- Create the Rolling Week Total and Rolling Week Average for the whole data set
- Pull the data together for the previous two requirements
- Output the data

Author: Kelly Gilbert
Created: 2021-07-29
Requirements:
  - input dataset:
      - PD 2021 Wk 26 Input - Sheet1.csv
  - output dataset (for results check only):
      - PD 2021 Wk 26 Output.csv
"""


from pandas import concat, merge, read_csv, Timedelta


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\inputs\PD 2021 Wk 26 Input - Sheet1.csv', parse_dates=['Date'], dayfirst=True)\
             .sort_values(by='Date')
       

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df['begin_date'] = df['Date'] - Timedelta('3 day')
df['end_date'] = df['Date'] + Timedelta('3 day')


# Create a data set that gives 7 rows per date (unless those dates aren't included in the data set). 
# Remove any additional fields you don't need 
# Create the Rolling Week Total and Rolling Week Average per destination


# method 1: cross join using merge
# this will join every date to every date for each destination
# faster, but more memory
df1 = df.merge(df, on='Destination', suffixes=['', '_r'], how='inner')
df1 = df1.loc[(df1['Date_r'] >= df1['begin_date']) & (df1['Date_r'] <= df1['end_date'])]
         
df_total1 = df1.groupby(['Destination', 'Date']).agg(Rolling_Week_Avg=('Revenue_r', 'mean'),
                                                     Rolling_Week_Total=('Revenue_r', 'sum'))\
               .reset_index()


# method 2: groupby (less memory, but slower)
# good if you have a small # of destinations and a large # of dates
# this performs the join one destination at a time
# source: https://stackoverflow.com/questions/23508351/how-to-do-workaround-a-conditional-join-in-python-pandas

def cond_merge(g): 
    g = g.merge(g, on='Destination', how='inner', suffixes=['', '_r'])
    g = g.loc[(g['Date_r'] >= g['begin_date']) & (g['Date_r'] <= g['end_date'])]
    return g.groupby(['Destination', 'Date']).agg(Rolling_Week_Avg=('Revenue_r', 'mean'),
                                                  Rolling_Week_Total=('Revenue_r', 'sum'))\
            .reset_index()

df_total2 = df.groupby('Destination').apply(cond_merge).reset_index(drop=True)
 

# create the Rolling Week Total and Rolling Week Average for the whole data set
# NOTE: to match the solution, this is an average of Destination averages
df_all = df_total2.groupby('Date').agg(Rolling_Week_Avg=('Rolling_Week_Avg', 'mean'),
                                       Rolling_Week_Total=('Rolling_Week_Total', 'sum'))\
                  .reset_index()
df_all['Destination'] = 'All'

df_all = concat([df_total2, df_all])
df_all.columns = df_all.columns = [c.replace('_', ' ') for c in df_all.columns]


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_all.to_csv(r'.\outputs\output-2021-26.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 26 Output.csv']
my_files = ['output-2021-26.csv']
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
