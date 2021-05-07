# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 14 - Prep Air In-Flight Purchases
https://preppindata.blogspot.com/2021/04/2021-week-14-prep-air-in-flight.html
 
- Input the Data
- Assign a label for where each seat is located.
  They are assigned as follows:
  A & F - Window Seats
  B & E - Middle Seats
  C & D - Aisle Seats 
- Combine the Seat List and Passenger List tables.
- Parse the Flight Details so that they are in separate fields
- Calculate the time of day for each flight.
  They are assigned as follows: 
  Morning - Before 12:00 
  Afternoon - Between 12:00 - 18:00
  Evening - After 18:00
- Join the Flight Details & Plane Details to the Passenger & Seat tables. We should be able to 
  identify what rows are Business or Economy Class for each flight.
- Answer the following questions: 
    - What time of day were the most purchases made? We want to take a look at the average for the
      flights within each time period.
    - What seat position had the highest purchase amount? Is the aisle seat the highest earner
      because it's closest to the trolley?
    - As Business Class purchases are free, how much is this costing us?
    - Bonus: If you have Tableau Prep 2021.1 or later, you can now output to Excel files. Can you
      combine all of the outputs into a single Excel workbook, with a different sheet for each 
      output?

Author: Kelly Gilbert
Created: 2021-05-07
Requirements: 
  - pandas version 0.25.0 or higher (for explode)
  - input dataset (Shopping List and Ingredients.xlsx)
  - output dataset (for results check):
    - Vegan List.csv
    - Non Vegan List.csv
  
"""


from pandas import ExcelFile, read_excel

# used for answer check only
from pandas import read_csv


# --------------------------------------------------------------------------------------------------
# input the data
# --------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\   .xlsx') as xl:
    s1 = read_excel(xl, 's1')
    ...


# --------------------------------------------------------------------------------------------------
# prep / calculations
# --------------------------------------------------------------------------------------------------




# --------------------------------------------------------------------------------------------------
# output the data
# --------------------------------------------------------------------------------------------------




# ---------------------------------------------------------------------------------------------------
# check results
# ---------------------------------------------------------------------------------------------------

solutionFiles = ['PD 2021 Wk 11 Output.csv']
myFiles = ['output-2021-11.csv']
col_order_matters = False


for i in range(len(solutionFiles)):
    print('\n---------- Checking \'' + myFiles[i] + '\' ----------\n')

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

        if len(dfCompare[dfCompare['in_solution'].isna() | dfCompare['in_mine'].isna()]) > 0:
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')

    print('\n')
