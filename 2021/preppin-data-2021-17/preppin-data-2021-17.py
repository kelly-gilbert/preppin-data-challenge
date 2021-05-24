# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 17 - Timesheet Checks
https://preppindata.blogspot.com/2021/04/week-17-timesheet-checks.html

- Input the data
- Remove the ‘Totals’ Rows
- Pivot Dates to rows and rename fields 'Date' and 'Hours'
- Split the ‘Name, Age, Area of Work’ field into 3 Fields and Rename
- Remove unnecessary fields
- Remove the row where Dan was on Annual Leave and check the data type of the Hours Field.
- Total up the number of hours spent on each area of work for each date by each employee.

- First we are going to work out the avg number of hours per day worked by each employee
  - Calculate the total number of hours worked and days worked per person
  - Calculate the avg hours and remove unnecessary fields.

- Now we are going to work out what % of their day (not including Chats) was spend on Client work.
  - Filter out Work related to Chats.
  - Calculate total number of hours spent working on each area for each employee
  - Calculate total number of hours spent working on both areas together for each employee
  - Join these totals together
  - Calculate the % of total and remove unnecessary fields
  - Filter the data to just show Client work
  - Join to the table with Avg hours to create your final output

Author: Kelly Gilbert
Created: 2021-05-23
Requirements:
  - input dataset:
      - Preppin Data Challenge.xlsx
  - output dataset (for results check):
      - PD 2021 Wk 17 Output.csv
"""


from pandas import ExcelFile, melt, read_excel

# for solution check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Preppin Data Challenge.xlsx') as xl:
    df = read_excel(xl)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# remove total rows
df = df.loc[df['Name, Age, Area of Work'].notna()]

# pivot dates to rows and rename fields 'Date' and 'Hours'
df_m = df.melt(id_vars=['Name, Age, Area of Work', 'Project'], var_name='Date', value_name='Hours')

# split the ‘Name, Age, Area of Work’ field into 3 Fields and Rename
df_m[['Name', 'Age', 'Area of Work']] = df_m.iloc[:, 0].str.extract('(.*), (\d+): (.*)')

# check for nulls
# df_m[(df_m['Name'].isna()) | (df_m['Age'].isna()) | (df_m['Area of Work'].isna())]

# remove unnecessary fields
df_m.drop(columns=['Name, Age, Area of Work'], inplace=True)

# remove the row where Dan was on Annual Leave and check the data type of the Hours Field
df_m = df_m.loc[df_m['Hours'] != 'Annual Leave']
df_m['Hours'] = df_m['Hours'].astype('float16')


# work out the avg number of hours per day worked by each employee
df_tot = df_m.groupby('Name').agg(total_days=('Date', 'nunique'),
                                  total_hours=('Hours', 'sum')).reset_index()
df_tot['Avg Number of Hours worked per day'] = df_tot['total_hours'] / df_tot['total_days']


# hours by name and area of work (excluding chats)
df_area = df_m[df_m['Area of Work'] != 'Chats']\
          .groupby(['Name', 'Area of Work'])['Hours'].sum().reset_index()


# % of non-chat hours
df_area['% of Total'] = (df_area['Hours'] / df_area.groupby('Name')['Hours'].transform('sum'))\
                        .map('{:.0%}'.format)


# add the totals
df_area = df_area.merge(df_tot, on='Name', how='left')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# output client work only
out_cols = ['Name', 'Area of Work', '% of Total', 'Avg Number of Hours worked per day']
df_area[df_area['Area of Work'] == 'Client'].to_csv(r'.\outputs\output-2021-17.csv', index=False,
                                                    columns=out_cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solutionFiles = ['PD 2021 Wk 17 Output.csv']
myFiles = ['output-2021-17.csv']
col_order_matters = False

for i in range(len(solutionFiles)):
    print('---------- Checking \'' + solutionFiles[i] + '\' ----------\n')

    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solutionFiles[i])
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
    