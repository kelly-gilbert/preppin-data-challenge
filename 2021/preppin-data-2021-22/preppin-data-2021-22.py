# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 22 - Answer Smash
https://preppindata.blogspot.com/2021/06/2021-week-22-answer-smash.html

- Input the data
- The category dataset requires some cleaning so that Category and Answer are 2 separate fields
- Join the datasets together, making sure to keep an eye on row counts
- Filter the data so that each answer smash is matched with the corresponding name and answer
- Remove unnecessary columns
- Output the data

Author: Kelly Gilbert
Created: 2021-06-03
Requirements:
  - input dataset:
      - Answer Smash Input.xlsx
  - output dataset (for results check only):
      - Answer Smash Output.csv
"""


from pandas import DataFrame, ExcelFile, read_excel

# for solution check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Answer Smash Input.xlsx') as xl:
    smash = read_excel(xl, 'Answer Smash')
    names = read_excel(xl, 'Names')
    questions = read_excel(xl, 'Questions')
    cat = read_excel(xl, 'Category')        
        

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# split the category data
cat = cat['Category: Answer'].str.strip().str.extract('(?P<Category>.*?)\: (?P<Answer>.*)', expand=True)

# find the name for each answer smash
smash['Name'] = [[n for n in names['Name'] if s.lower().startswith(n.lower())] 
                 for s in smash['Answer Smash']]
smash = smash.explode('Name')

# find the answer for each answer smash
smash['Answer'] = [[a for a in cat['Answer'] if s.lower().endswith(a.lower())] 
                   for s in smash['Answer Smash']] 
smash = smash.explode('Answer')

# join the answer smash to the questions
smash = smash.merge(questions, on='Q No', how='left', indicator=True)


# check joins
check = smash.groupby('Answer Smash')['Name'].agg(Names=('Name', 'nunique')).reset_index()
if len(check[check['Names'] < 1]) > 0:
    print('The following answer smashes did not match to a name:\n')
    print(check[check['Names'] == 1], end='\n\n')

if len(check[check['Names'] > 1]) > 0:
    print('The following answer smashes matched to multiple names:\n')
    print(check[check['Names'] > 1], end='\n\n')

check = smash.groupby('Answer Smash')['Answer'].agg(Answers=('Answer', 'nunique')).reset_index()
if len(check[check['Answers'] < 1]) > 0:
    print('The following answer smashes did not match to an answer:\n')
    print(check[check['Answers'] < 1], end='\n\n')

if len(check[check['Answers'] > 1]) > 0:
    print('The following answer smashes matched to multiple answers:\n')
    print(check[check['Answers'] > 1], end='\n\n')

if len(smash[smash['_merge'] != 'both']) > 0:
    print('The following answer smashes did not match anything in the Questions list:\n')
    print(smash[smash['_merge'] != 'both'])
    print('\n\n')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Q No', 'Name', 'Question', 'Answer', 'Answer Smash']
smash.to_csv(r'.\outputs\output-2021-22.csv', index=False, columns=out_cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Answer Smash Output.csv']
my_files = ['output-2021-22.csv']
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
