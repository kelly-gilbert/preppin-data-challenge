# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 5 The Prep School - Setting Grades
https://preppindata.blogspot.com/2022/02/2022-week-5-prep-school-setting-grades.html

- Input data
- Divide the students grades into 6 evenly distributed groups (have a look at 'Tiles' functionality in Prep)
    - By evenly distributed, it means the same number of students gain each grade within a subject
- Convert the groups to two different metrics:
    - The top scoring group should get an A, second group B etc through to the sixth group who receive an F
    - An A is worth 10 points for their high school application, B gets 8, C gets 6, D gets 4, 
      E gets 2 and F gets 1.
- Determine how many high school application points each Student has received across all their subjects 
- Work out the average total points per student by grade 
    - ie for all the students who got an A, how many points did they get across all their subjects
- Take the average total score you get for students who have received at least one A and remove 
  anyone who scored less than this. 
- Remove results where students received an A grade (requirement updated 2/2/22)
- How many students scored more than the average if you ignore their As?
- Output the data

Author: Kelly Gilbert
Created: 2022-02-02
Requirements:
  - input dataset:
      - PD 2022 Wk 5 Input.csv
  - output dataset (for results check only):
      - PD 2022 Wk 5 Output.csv
"""


import pandas as pd


#---------------------------------------------------------------------------------------------------
# set variables
#---------------------------------------------------------------------------------------------------

grade_map = {'A' : 10, 'B' : 8, 'C' : 6, 'D' : 4, 'E' : 2, 'F' : 1}


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\PD 2022 Wk 5 Input.csv')\
       .melt(id_vars='Student ID', var_name='Subject', value_name='Score')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# divide the grades into 6 evenly-distributed groups, add the grade letter and points
df['Grade'] = df.groupby('Subject')['Score']\
                .transform(lambda x: pd.qcut(x, q=6, labels=['F', 'E', 'D', 'C', 'B', 'A']))

df['Points'] = df['Grade'].replace(grade_map)


# determine how many high school application points each Student has received across all subjects
df['Total Points per Student'] = df.groupby('Student ID')['Points'].transform('sum')


# work out the average total points per student by grade 
# [KLG: I assumed this is weighted by number of grades, i.e. if a student had Bs in three subjects,
# then that student counts 3x in the B average. This produced results similar to the solution.]
df['Avg student total points per grade'] = df.groupby('Grade')['Total Points per Student']\
                                             .transform('mean')


# take the average total score you get for students who have received at least one A
# remove anyone who scored less than this. 
# remove results where a student received an A grade
avg_with_a = df[df['Grade']=='A']['Avg student total points per grade'].min()

df = df.loc[(df['Total Points per Student'] >= avg_with_a) & (df['Grade'] != 'A')]


# How many students scored more than the average if you ignore their As?
df['Points per Student without As'] = df.groupby('Student ID')['Points'].transform('sum')

df[df['Points per Student without As'] > avg_with_a]


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2022-05.csv', index=False, 
          columns=['Avg student total points per grade', 'Total Points per Student', 'Grade', 
                   'Points', 'Subject', 'Score', 'Student ID'])


#---------------------------------------------------------------------------------------------------
# alternative grade cut
#---------------------------------------------------------------------------------------------------

# the method I used above gives the same grade to all students who received a score, so the number
#   of students with each grade may not be exactly equal
# the provided solution cuts strictly into evenly-sized groups, so sometimes the breakpoint can 
#   occur with in a score (i.e. students with the same score could receive different letter grades)
# the method below will allow breaks within a score, like the solution.

df['Grade'] = df.groupby('Subject')['Score'].rank(method='first')\
                .transform(lambda x: pd.qcut(x, q=6, labels=['F', 'E', 'D', 'C', 'B', 'A']))


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# NOTE: the code above will produce slightly different results than the provided solution
# due to the difference in grade breakpoints

solution_files = ['PD 2022 Wk 5 Output.csv']
my_files = ['output-2022-05.csv']
unique_cols = [['Student ID', 'Subject']]
col_order_matters = False
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
        errors = 0
        df_compare = df_sol.merge(df_mine, how='outer', on=unique_cols[i],
                                  suffixes=['_sol', '_mine'], indicator=True)
        
        # extra/missing records
        if len(df_compare[df_compare['_merge'] != 'both']) > 0:
            print('*** Missing or extra records ***\n')
            print('In solution, not in mine:\n')
            print(df_compare[df_compare['_merge'] == 'left_only'][unique_cols[i]])
            print('\n\nIn mine, not in solution:\n')
            print(df_compare[df_compare['_merge'] == 'right_only'][unique_cols[i]]) 
            errors += 1

        # for the records that matched, check for mismatched values
        for c in [c for c in df_sol.columns if c not in unique_cols[i]]:
            if 'float' in df_compare[f'{c}_sol'].dtype.name:
                df_compare[f'{c}_sol'] = df_compare[f'{c}_sol'].round(round_dec)
                df_compare[f'{c}_mine'] = df_compare[f'{c}_mine'].round(round_dec)
                
            unmatched = df_compare[(df_compare['_merge']=='both')
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]
            if len(unmatched) > 0:
                print(f'\n\n*** Values do not match: {c} ***\n')
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                errors += 1
        
        if errors == 0:
            print('Values match')

    print('\n')  
