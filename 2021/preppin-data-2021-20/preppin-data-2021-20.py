# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 20 - Controlling Complaints
https://preppindata.blogspot.com/2021/05/2021-week-20-controlling-complaints.html

- Input the data file
- Create the mean and standard deviation for each Week
- Create the following calculations for each of 1, 2 and 3 standard deviations:
    - The Upper Control Limit (mean+(n*standard deviation))
    - The Lower Control Limit (mean-(n*standard deviation))
    - Variation (Upper Control Limit - Lower Control Limit)
- Join the original data set back on to these results
- Assess whether each of the complaint values for each Department, Week and Date is within or 
  outside of the control limits
- Output only Outliers
- Produce a separate output worksheet (or csv) for 1, 2 or 3 standard deviations and remove the 
  irrelevant fields for that output.

Author: Kelly Gilbert
Created: 2021-05-31
Requirements:
  - input dataset:
      - Prep Air Complaints - Complaints per Day.csv
  - output dataset (for results check):
      - PD 2021 Wk 20 Output.xlsx
"""


from numpy import where
from pandas import DataFrame, ExcelWriter, read_csv

# for solution check only
from pandas import ExcelFile, read_excel


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\inputs\Prep Air Complaints - Complaints per Day.csv',
              parse_dates=['Date'], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create the mean and standard deviation for each Week
df_wk = df.groupby('Week').agg(Mean=('Complaints', 'mean'),
                               stdev=('Complaints', 'std')).reset_index()

# duplicate the weekly dataframe for each number of standard deviations
stdev_values = [1, 2, 3]

df_wk['join'] = 1
df_wk = df_wk.merge(DataFrame({'n' : stdev_values, 'join' : [1]*len(stdev_values)}), on='join')

# calculate the control limits for 1, 2, and 3 standard deviations
df_wk['ucl'] = df_wk['Mean'] + df_wk['n'] * df_wk['stdev']
df_wk['lcl'] = df_wk['Mean'] - df_wk['n'] * df_wk['stdev']
df_wk['Variation'] = df_wk['ucl'] - df_wk['lcl']

# join back to the original dataset
df_all = df.merge(df_wk, on='Week')

# assess whether each of the complaint values is within or outside of the control limits
df_all['Outlier?'] = where((df_all['Complaints'] > df_all['ucl'])
                           | (df_all['Complaints'] < df_all['lcl']), 'Outlier', 0)

# keep only outliers
df_outliers = df_all.loc[df_all['Outlier?']=='Outlier']


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_outliers.rename(columns={'ucl':'Upper Control Limit', 'lcl':'Lower Control Limit',
                            'stdev':'Standard Deviation'}, inplace=True)

out_cols = ['Variation', 'Outlier?', 'Lower Control Limit', 'Upper Control Limit',
            'Standard Deviation', 'Mean', 'Date', 'Week', 'Complaints', 'Department']

with ExcelWriter(r'.\outputs\output-2021-20.xlsx') as w:

    # cycle through the number of std deviations, outputting a separate tab for each
    for n in df_outliers['n'].unique():
        df_out = df_outliers.loc[df_outliers['n']==n][out_cols]
        df_out.columns = [c + ' (' + str(n) + 'SD)' 
                          if c in ['Lower Control Limit', 'Outlier?', 'Upper Control Limit', 
                                   'Variation'] else c for c in df_out.columns]
        df_out.to_excel(w, str(n) + ' SD', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solutionFiles = ['PD 2021 Wk 20 Output - Copy.xlsx']
    # NOTE: the solution file had inconsistent column naming across tabs (Outlier? vs Outlier,
    #       (nSD) present sometimes, 'Outside' vs. 'Outlier' in the outlier column), so I manually
    #       adjusted the ' - Copy' version to be consistent
myFiles = ['output-2021-20.xlsx']
col_order_matters = False

for i, solution_file in enumerate(solutionFiles):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    f_solution = ExcelFile('.\\outputs\\' + solution_file)
    f_mine = ExcelFile('.\\outputs\\' + myFiles[i])

    # check sheet names    
    if sorted(f_mine.sheet_names) != sorted(f_solution.sheet_names):
        print('*** Sheets do not match ***')
        print('    Sheets in solution: ' + str(sorted(f_solution.sheet_names)))
        print('    Sheets in mine    : ' + str(sorted(f_mine.sheet_names)))
        col_match = False
        break
    else:
        print('    Sheet names match\n')

    # cycle through the sheets
    for s in f_solution.sheet_names:          
        
        print('    ---- Checking sheet ' + s + ' --------------------\n')
        dfSolution = read_excel(f_solution, s)
        dfMine = read_excel(f_mine, s)
    
        # are the fields the same and in the same order?        
        solutionCols = list(dfSolution.columns)
        myCols = list(dfMine.columns)
        if not col_order_matters:
             solutionCols.sort()
             myCols.sort()
    
        col_match = False
        if solutionCols != myCols:
            print('    *** Columns do not match ***')
            print('        Columns in solution: ' + str(solutionCols))
            print('        Columns in mine    : ' + str(myCols))
        else:
            print('    Columns match\n')
            col_match = True
    
        # are the values the same? (only check if the columns matched)
        if col_match:
            # round floats to 8 decimal places for match
            for c in dfSolution.columns:
                if 'float' in str(dfSolution[c].dtype): 
                    dfSolution[c] = dfSolution[c].round(8)
                    dfMine[c] = dfMine[c].round(8)

            dfSolution['join'] = 1
            dfMine['join'] = 1
            dfCompare = dfSolution.merge(dfMine, how='outer', on=list(dfSolution.columns)[:-1])
            dfCompare.rename(columns={'join_x':'in_solution', 'join_y':'in_mine'}, inplace=True)
    
            if dfCompare['in_solution'].count() != len(dfCompare):
                print('    *** Values do not match ***')
                print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
            else:
                print('    Values match')
    
        print('\n')
