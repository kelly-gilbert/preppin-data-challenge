# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2021-05
https://preppindata.blogspot.com/2021/02/2021-week-5-dealing-with-duplication.html
 
Dealing with duplication

- Input the data 
- For each Client, work out who the most recent Account Manager is
- Filter the data so that only the most recent Account Manager remains
- Be careful not to lose any attendees from the training sessions!
- In some instances, the Client ID has changed along with the Account Manager. Ensure only the most 
  recent Client ID remains
- Output the data

Author: Kelly Gilbert
Created: 2021-02-06
Requirements: 
  - input dataset (Joined Dataset.csv)
  - output dataset (for results check):
    - Current AM Dataset.csv
  
"""


from pandas import merge, read_csv

# input the data
df = read_csv('.\\inputs\\Joined Dataset.csv', parse_dates=['From Date'], dayfirst=True)

# find the current Account Manager, client ID, and from date for each client name
outCols = ['Client ID', 'Account Manager', 'From Date']
dfCurrentAM = df.sort_values(by='From Date').groupby('Client')[outCols].last().reset_index()

# deduplicate the attendee data
outCols = ['Training', 'Contact Email', 'Contact Name', 'Client']
dfDeduped = df.drop_duplicates(subset=outCols)[outCols]

# join to get the current Account Manager and Client ID
dfFinal = dfDeduped.merge(dfCurrentAM, how='left', on='Client')

# output the data
dfFinal.to_csv('.\\outputs\\output-2021-05.csv', index=False)


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solution_files = ['Current AM Dataset.csv']
my_files = ['output-2021-05.csv']
col_order_matters = False

for i in range(len(solution_files)):
    print('---------- Checking \'' + solution_files[i] + '\' ----------\n')
    
    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_files[i], parse_dates=['From Date'], dayfirst=True)
    df_mine = read_csv('.\\outputs\\' + my_files[i], parse_dates=['From Date'])
    
    # are the fields the same and in the same order?
    solution_cols = list(df_solution.columns)
    my_cols = list(df_mine.columns)
    if col_order_matters == False:
         solution_cols.sort()
         my_cols.sort()

    col_match = False
    if solution_cols != my_cols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_solution.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
    else:
        print('Columns match\n')
        col_match = True
    
    # are the values the same? (only check if the columns matched)
    if col_match == True:
        df_solution['check'] = 1
        df_mine['check'] = 1
        df_compare = df_solution.merge(df_mine, how='outer', on=list(df_solution.columns)[:-1])
        
        if df_compare['check_x'].count() != len(df_compare):
            print('*** Values do not match ***')
            print(df_compare[df_compare['check_x'] != df_compare['check_x']])
        else:
            print('Values match')
    
    print('\n')