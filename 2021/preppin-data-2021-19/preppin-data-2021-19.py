# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 19 - Prep Air Project Details
https://preppindata.blogspot.com/2021/05/2021-week-19-prep-air-project-details.html

- Input the data
- There are lots of different ways you can do this challenge so rather than a step-by-step set of
  requirements, feel free to create each of these data fields in whatever order you like:
    - 'Week' with the word week and week number together 'Week x'
    - 'Project' with the full project name
    - 'Sub-Project' with the full sub-project name
    - 'Task' with the full type of task
    - 'Name' with the owner of the task's full name (Week 18's output can help you check these
      if needed)
    - 'Days Noted' some fields have comments that say how many days tasks might take. This field
      should note the number of days mentioned if said in the comment otherwise leave as a null.
    - 'Detail' the description from the system output with the project details in the [ ]
- Output the file

Author: Kelly Gilbert
Created: 2021-05-28
Requirements:
  - input dataset:
      - PD 2021 Wk 19 Input.xlsx
  - output dataset (for results check):
      - PD 2021 Wk 19 Output.csv
"""


from pandas import ExcelFile, merge, read_excel

# for solution check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\PD 2021 Week 19 Input.xlsx') as xl:
    df = read_excel(xl, 'Project Schedule Updates')
    proj = read_excel(xl, 'Project Lookup Table')
    subproj = read_excel(xl, 'Sub-Project Lookup Table')
    task = read_excel(xl, 'Task Lookup Table')
    owner = read_excel(xl, 'Owner Lookup Table')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# 'Week' with the word week and week number together 'Week x'
df.index = 'Week ' + df['Week'].astype(str)

# split projects into rows (split on space that is followed by [)
df = df['Commentary'].str.split('\s+(?=\[)').explode().str.strip().reset_index()

# parse the commentary
df[['Project Code', 'Sub-Project Code', 'Task Code', 'Detail']] = \
                       df['Commentary'].str.extract('\[(.*?)\/(.*?)\-(.*?)\]\s+(.*)\s?')

# parse the owner name
df['Abbreviation'] = df['Detail'].str.extract('.*\s(.*)\.\s*')

# adjust case
df['Sub-Project Code'] = df['Sub-Project Code'].str.lower().replace('ops', 'op')
df['Abbreviation'] = df['Abbreviation'].str.title()

# parse the days noted
df['Days Noted'] = df['Detail'].str.extract('.*?(\d+)\sday.*')


# join to the lookup tables
df = df.merge(proj, on='Project Code', how='left')\
       .merge(subproj, on='Sub-Project Code', how='left')\
       .merge(task, on='Task Code', how='left')\
       .merge(owner, on='Abbreviation', how='left')


# check for misjoins
if len(df[df['Project'].isna()]) > 0:
    print('The following records did not match to the Project lookup:\n' 
          + str(list(df[df['Project'].isna()]['Project Code'].unique())) + '\n')

if len(df[df['Sub-Project'].isna()]) > 0:
    print('The following records did not match to the Sub-Project lookup:\n' 
          + str(list(df[df['Project'].isna()]['Sub-Project Code'].unique())) + '\n')

if len(df[df['Task'].isna()]) > 0:
    print('The following records did not match to the Task lookup:\n' 
          + str(list(df[df['Project'].isna()]['Task Code'].unique())) + '\n')

if len(df[df['Name'].isna()]) > 0:
    print('The following records did not match to the Owner lookup:\n' 
          + str(list(df[df['Project'].isna()]['Abbreviation'].unique())) + '\n')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Week', 'Project', 'Sub-Project', 'Task', 'Name', 'Days Noted', 'Detail']
df.to_csv(r'.\outputs\output-2021-19.csv', index=False, columns=out_cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solutionFiles = ['PD 2021 Wk 19 Output.csv']
myFiles = ['output-2021-19.csv']
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
