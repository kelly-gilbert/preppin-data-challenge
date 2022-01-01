# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 52 - Departmental December Operations
https://preppindata.blogspot.com/2021/12/2021-week-52-departmental-december.html?m=1

- Input data
- Count the number of complaints per customer
- Join the 'Department Responsible' data set to allocate the complaints to the correct department
- Create a comma-separated field for all the keywords found in the complaint for each department
- For any complaint that isn't classified, class the department as 'unknown' and the complaint 
  cause as 'other'
- Output the data

Author: Kelly Gilbert
Created: 2021-12-29
Requirements:
  - input dataset:
      - PD 2021 Wk 52 Input.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 52 Output.csv
"""


from pandas import ExcelFile, read_excel


# for results check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\inputs\PD 2021 Wk 52 Input.xlsx') as xl:
    df_comp = read_excel(xl, 'Complaints')
    df_dept = read_excel(xl, 'Department Responsbile')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# count the number of complaints by customer
df_comp['Complaints per Person'] = df_comp.groupby('Name')['Complaint'].transform('size')


# preprocess the Complaint text
df_comp['Complaint'] = df_comp['Complaint'].str.strip().str.lower()


# find keyword matches and split them into rows; merge to get the department name for each keyword
keywords = '|'.join(df_dept['Keyword'].str.lower())
df_out = df_comp.assign(Keyword=df_comp['Complaint'].str.findall(keywords))\
                .explode('Keyword')\
                .merge(df_dept.assign(Keyword=df_dept['Keyword'].str.lower()), on='Keyword', how='left')


# for any complaint that isn't classified, class the department as 'unknown' and 'other' cause
df_out['Complaint causes'] = df_out['Keyword'].fillna('other')
df_out['Department'] = df_out['Department'].fillna('Unknown')


# create a comma-separated list of keywords grouped by department
df_out = df_out.groupby(['Name', 'Complaint', 'Department', 'Complaints per Person'])['Complaint causes']\
               .agg(lambda x: ', '.join(x))\
               .reset_index()


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2021-52.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 52 Output.csv']
my_files = ['output-2021-52.csv']
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
