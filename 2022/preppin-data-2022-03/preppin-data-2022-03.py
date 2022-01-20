# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 3 The Prep School - Passing Grades
https://preppindata.blogspot.com/2022/01/2022-week-3-prep-school-passing-grades.html

- Input both data sets
- Join the data sets together to give us the grades per student
- Remove the parental data fields, they aren't needed for the challenge this week
- Pivot the data to create one row of data per student and subject
- Rename the pivoted fields to Subject and Score 
- Create an average score per student based on all of their grades
- Create a field that records whether the student passed each subject
- Pass mark is 75 and above in all subjects
- Aggregate the data per student to count how many subjects each student passed
- Round the average score per student to one decimal place
- Remove any unnecessary fields and output the data

Author: Kelly Gilbert
Created: 2022-01-19
Requirements:
  - input datasets:
      - PD 2022 Wk 1 Input - Input.csv
      - PD 2022 WK 3 Grades.csv
  - output dataset (for results check only):
      - PD 2022 Wk 3 Output.csv
"""


import pandas as pd


PASSING_SCORE = 75


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_students = pd.read_csv(r'.\inputs\PD 2022 Wk 1 Input - Input.csv', usecols=['id', 'gender'])\
                .rename(columns={'id' : 'Student ID', 'gender' : 'Gender'})
       
df_grades = pd.read_csv(r'.\inputs\PD 2022 WK 3 Grades.csv')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# join the data sets together to give us the grades per student
df = df_students.merge(df_grades.melt(id_vars='Student ID', var_name='Subject', value_name='Score'),
                       on='Student ID', how='left')\
                .assign(Pass=lambda df_x: df_x['Score'] >= PASSING_SCORE)


# create an average score per student based on all of their grades
df_out = df.groupby(['Student ID', 'Gender']).agg(Passed_Subjects=('Pass', 'sum'),
                                                  Avg_Score=('Score', 'mean'))\
           .reset_index()\
           .assign(Avg_Score=lambda df_x: df_x['Avg_Score'].round(1))\
           .rename(columns={'Passed_Subjects' : 'Passed Subjects', 
                            'Avg_Score' : 'Student\'s Avg Score'})


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-03.csv', index=False, 
              columns=['Passed Subjects', 'Student\'s Avg Score', 'Student ID', 'Gender'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2022 Wk 3 Output.csv']
my_files = ['output-2022-03.csv']
unique_cols = ['Student ID']
col_order_matters = True
round_dec = 8


for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_sol = pd.read_csv('.\\outputs\\' + solution_file)
    df_mine = pd.read_csv('.\\outputs\\' + my_files[i])

    # are the columns the same?
    solution_cols = list(df_sol.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_sol.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
        print('\n\n')
    else:
        print('Columns match\n')
        col_match = True


    # are the values the same? (only check if the columns matched)
    if col_match:
        df_compare = df_sol.merge(df_mine, how='outer', on=unique_cols,
                                  suffixes=['_sol', '_mine'], indicator=True)
        
        # extra/missing records
        if len(df_compare[df_compare['_merge'] != 'both']) > 0:
            print('*** Missing or extra records ***\n')
            print('In solution, not in mine:\n')
            print(df_compare[df_compare['_merge'] == 'left_only'][unique_cols])
            print('\n\nIn mine, not in solution:\n')
            print(df_compare[df_compare['_merge'] == 'right_only'][unique_cols]) 


        # for the records that matched, check for mismatched values
        unmatched_cols = 0
        for c in [c for c in df_sol.columns if c not in unique_cols]:
            if 'float' in df_compare[f'{c}_sol'].dtype.name:
                df_compare[f'{c}_sol'] = df_compare[f'{c}_sol'].round(round_dec)
                df_compare[f'{c}_mine'] = df_compare[f'{c}_mine'].round(round_dec)
                
            unmatched = df_compare[(df_compare['_merge']=='both')
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]
            if len(unmatched) > 0:
                print(f'*** Values do not match: {c} ***\n')
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                unmatched_cols += 1
        
        if unmatched_cols == 0:
            print('Values match')

    print('\n')  
