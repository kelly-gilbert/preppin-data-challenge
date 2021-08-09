# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 27 - NBA Draft Lottery calculator
https://preppindata.blogspot.com/2021/07/2021-week-27-nba-draft-lottery.html

- Create a workflow that will allocate the draft picks in a random manner based on the odds for 
  each team
- The workflow should allocate each of the first 4 picks based on the lottery odds and then allocate
  all teams that didn't receive a slot to the remaining places in order
- Output the data


Author: Kelly Gilbert
Created: 2021-08-09
Requirements:
  - input dataset:
      - PD 2021 Wk 27 Input.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 27 Output - PD 2021 Wk 27 Output.csv
"""


from pandas import DataFrame, ExcelFile, melt, merge, read_excel
from random import choices

# for solution check only
from pandas import read_csv


# setup variables
lottery_count = 4    # the number to pick via lottery


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\inputs\PD 2021 Wk 27 Input.xlsx') as xl:
    prob = read_excel(xl, 'Seeding')
    teams = read_excel(xl, 'Teams')
        

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# melt pick probabilities into rows and convert to numbers
prob = melt(prob, id_vars=['Seed'], var_name='pick', value_name='prob').dropna()
prob['prob'] = prob['prob'].astype(str).str.replace('>', '').astype(float)


# select the first four picks by lottery
lottery = []
#pick = 0
for pick in range(lottery_count):
    
    # subset the probability table and randomly select a seed based on the weights
    prob_sub = prob.loc[(prob['pick']==pick+1) & ~prob['Seed'].isin(lottery)]
    lottery.append(choices(list(prob_sub['Seed']), weights=list(prob_sub['prob']))[0])


# add the remaining teams in seed order and join to the Teams list for final output
output = DataFrame({'Actual Pick' : range(1,len(teams)+1),
                    'Seed' : lottery + [t for t in teams['Seed'].sort_values() if t not in lottery]})\
             .merge(teams, on='Seed')\
             .sort_values(by='Actual Pick')\
             .rename(columns={'Seed' : 'Original'})


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

output.to_csv(r'.\outputs\output-2021-27.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# NOTE: only the columns are checked this week; values were checked by visual inspection,
#       since the random lottery selections can vary by run

solution_files = ['PD 2021 Wk 27 Output - PD 2021 Wk 27 Output.csv']
my_files = ['output-2021-27.csv']
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
