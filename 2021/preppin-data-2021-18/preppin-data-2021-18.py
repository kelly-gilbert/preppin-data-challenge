# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 18 - Prep Air Project Overruns
https://preppindata.blogspot.com/2021/05/2021-week-18-prep-air-project-overruns.html

- Input the data
- Workout the 'Completed Date' by adding on how many days it took to complete each task from the
  Scheduled Date
- Rename 'Completed In Days from Schedule Date' to 'Days Difference to Schedule'
- Your workflow will likely branch into two at this point:

- 1. Pivot Task to become column headers with the Completed Date as the values in the column
    - You will need to remove some data fields to ensure the result of the pivot is a single row for
      each project, sub-project and owner combination.
    - Calculate the difference between Scope to Build time
    - Calculate the difference between Build to Delivery time
    - Pivot the Build, Deliver and Scope column to re-create the 'Completed Dates' field and
      Task field
    - You will need to rename these
- 2. You don't need to do anything else to this second flow

- Now you will need to:
    - Join Branch 1 and Branch 2 back together
      Hint: there are 3 join clauses for this join
    - Calculate which weekday each task got completed on as we want to know whether these are
      during the weekend or not for the dashboard
    - Clean up the data set to remove any fields that are not required.
- Output as a csv file

Author: Kelly Gilbert
Created: 2021-05-26
Requirements:
  - input dataset:
      - PD 2021 Wk 18 Input.xlsx
  - output dataset (for results check):
      - PD 2021 Wk 18 Output.csv
"""


from pandas import ExcelFile, pivot_table, read_excel, Timedelta


# for solution check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\PD 2021 Wk 18 Input.xlsx') as xl:
    df = read_excel(xl)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# rename days difference column
df.rename(columns={'Completed In Days from Scheduled Date' : 'Days Difference to Schedule'},
          inplace=True)

# work out the 'Completed Date'
df['Completed Date'] = df['Scheduled Date'] \
                       + df['Days Difference to Schedule'].apply(lambda x: Timedelta(x, unit='D'))

# check for multiple rows
id_vars = ['Project', 'Sub-project', 'Owner']
df_check = df.groupby(id_vars + ['Task']).agg(count=('Scheduled Date', 'count')).reset_index()
if len(df_check[df_check['count'] > 1]) > 0:
    print('ERROR: the folowing Project/Sub-project/Owner/Task combinations have more than one row.')
    print('       The latest date for each combination was used\n')
    print(df_check)

# pivot task into columns
df_complete = df.pivot_table(index=id_vars, columns='Task', values='Completed Date', aggfunc='max')\
                .reset_index()

# calculate time differences
df_complete['Scope to Build Time'] = (df_complete['Build'] - df_complete['Scope']).dt.days
df_complete['Build to Delivery Time'] = (df_complete['Deliver'] - df_complete['Build']).dt.days

# merge the new cols into the original dataframe
df = df.merge(df_complete[id_vars + ['Scope to Build Time', 'Build to Delivery Time']], on=id_vars,
              how='inner')

# calculate the completed weekday
df['Completed Weekday'] = df['Completed Date'].dt.day_name()


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Completed Weekday', 'Task', 'Scope to Build Time', 'Build to Delivery Time',
            'Days Difference to Schedule', 'Project', 'Sub-project', 'Owner', 'Scheduled Date',
            'Completed Date']
df.to_csv(r'.\outputs\output-2021-18.csv', index=False, columns=out_cols, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solutionFiles = ['PD 2021 Wk 18 Output.csv']
myFiles = ['output-2021-18.csv']
col_order_matters = False

for i, solution_file in enumerate(solutionFiles):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solution_file)
    dfMine = read_csv('.\\outputs\\' + myFiles[i])

    # are the fields the same and in the same order?
    solutionCols = list(dfSolution.columns)
    myCols = list(dfMine.columns)
    if not col_order_matters:
         solutionCols.sort()
         myCols.sort()

    col_match = False
    if solutionCols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(dfSolution.columns)))
        print('    Columns in mine    : ' + str(list(dfMine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        dfSolution['join'] = 1
        dfMine['join'] = 1
        dfCompare = dfSolution.merge(dfMine, how='outer', on=list(dfSolution.columns)[:-1])
        dfCompare.rename(columns={'join_x':'in_solution', 'join_y':'in_mine'}, inplace=True)

        if dfCompare['in_solution'].count() != len(dfCompare):
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')

    print('\n')
