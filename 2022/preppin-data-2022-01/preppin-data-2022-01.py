# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 1 The Prep School - Parental Contact Details
https://preppindata.blogspot.com/2022/01/2022-week-1-prep-school-parental.html

- Input the csv file (link above)
- Form the pupil's name correctly for the records in the format Last Name, First Name
- Form the parental contact's name in the same format as the pupil's 
- Create the email address to contact the parent using the format 
  Parent First Name.Parent Last Name@Employer.com
- Create the academic year the pupils are in
- Each academic year starts on 1st September.
- Year 1 is anyone born after 1st Sept 2014 
- Year 2 is anyone born between 1st Sept 2013 and 31st Aug 2014 etc
- Remove any unnecessary columns of data
- Output the data

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input dataset:
      - PD 2022 Wk 1 Input - Input.csv
  - output dataset (for results check only):
      - PD 2022 Wk 1 Output.csv
"""


from numpy import where
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\inputs\PD 2022 Wk 1 Input - Input.csv', parse_dates=['Date of Birth'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# form the pupil's name correctly for the records in the format Last Name, First Name
df["Pupil's Name"] = df['pupil last name'] + ', ' + df['pupil first name']

# form the parental contact's name in the same format as the pupil's 
df['Parental Contact Use'] = where(df['Parental Contact']==1, df['Parental Contact Name_1'],
                                   df['Parental Contact Name_2'])
df['Parental Contact Full Name'] = df['pupil last name'] + ', ' + df['Parental Contact Use']


# create the email address to contact the parent: Parent First Name.Parent Last Name@Employer.com
df['Parental Contact Email Address'] = df['Parental Contact Use'] + '.' + df['pupil last name']\
                                       + '@' + df['Preferred Contact Employer'] + '.com'

# create the academic year the pupils are in (each academic year starts on 1st September)
df['Academic Year'] = where(df['Date of Birth'] >= '2014-09-01', 1, 
                            (2015 - df['Date of Birth'].dt.year) 
                            + where(df['Date of Birth'].dt.month < 9, 1, 0))


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

cols = ['Academic Year', "Pupil's Name", 'Parental Contact Full Name', 'Parental Contact Email Address']
df.to_csv(r'.\outputs\output-2022-01.csv', index=False, columns=cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2022 Wk 1 Output.csv']
my_files = ['output-2022-01.csv']
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
