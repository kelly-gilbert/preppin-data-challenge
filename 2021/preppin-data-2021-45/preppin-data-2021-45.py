# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 45 - Spread the Knowledge for TC
https://preppindata.blogspot.com/2021/11/2021-week-45-spread-knowledge-for-tc.html

- Input the Data
- Create a DateTime field for each Session
- Create a row for each Attendee and Join on the Lookup Table
- Create a Direct Contact Field for each Attendee 
    - These are people they directly meet in the brain dates they attend
- Make sure Attendees don't have their own names listed as Direct Contacts
- Create an Indirect Contact field for each Attendee
    - These will be the Direct Contacts for each Attendee's Direct Contacts, for sessions that have
      happened prior to the session where they meet
    - Remember: order of sessions is important!
- If another attendee is classified as both a Direct and an Indirect Contact, classify them as a 
  Direct Contact
- Reshape the data so that each row represents an attendee and a contact they've made, either 
  Directly or Indirectly, for each subject matter
    - Ensure there are no duplicates!
- Output the Data

Author: Kelly Gilbert
Created: 2021-11-17
Requirements:
  - input dataset:
      - TC Input.xlsx
  - output dataset (for results check only):
      - TC Output.csv
"""


from pandas import concat, DataFrame, ExcelFile, merge, read_excel, to_datetime

# for results check only:
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\inputs\TC Input.xlsx') as xl:
    df = concat([read_excel(xl, s).assign(date=s) for s in xl.sheet_names if s != 'Attendees'])\
        .rename(columns={'Attendee IDs' : 'Attendee ID'})
    df_att = read_excel(xl, 'Attendees', )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create a DateTime field for each Session
df['DateTime'] = to_datetime(df['date'] + ' 2021 ' 
                             + (df['Session Time'].astype(str) + ':00:00').str[0:8])
df.drop(columns=['date', 'Session Time'], inplace=True)


# split attendees into rows
df['Attendee ID'] = df['Attendee ID'].str.split(', ')
df = df.explode('Attendee ID').astype({'Attendee ID' : 'int'})


# join on session ID to get direct contacts (people who attended the same session)
dc = df.merge(df[['Session ID', 'Attendee ID']], on='Session ID', suffixes=['', '_2'])
dc.drop(dc.loc[dc['Attendee ID'] == dc['Attendee ID_2']].index, axis=0, inplace=True)


# join on direct contact ID to get their direct contacts
ic = dc[['Subject', 'DateTime', 'Attendee ID', 'Attendee ID_2']]\
     .merge(dc, left_on=['Subject', 'Attendee ID_2'], right_on=['Subject', 'Attendee ID'],
            suffixes=['', '_ic'])

ic = ic.drop(ic.loc[(ic['Attendee ID'] == ic['Attendee ID_2_ic'])
                    | (ic['DateTime'] < ic['DateTime_ic'])].index)\
       [['Subject', 'Attendee ID', 'Attendee ID_2_ic']]\
       .rename(columns={'Attendee ID_2_ic' : 'Attendee ID_2'})


# union direct and indirect contacts, add the attendee names, remove any duplicates
cols = ['Subject', 'Attendee ID', 'Attendee ID_2']
df_all = concat([dc[cols].drop_duplicates(subset=['Subject', 'Attendee ID', 'Attendee ID_2'])\
                         .assign(Contact_Type='Direct Contact'),
                 ic[cols].assign(Contact_Type='Indirect Contact')], axis=0)\
         .sort_values(by='Contact_Type')\
         .drop_duplicates(subset=['Subject', 'Attendee ID', 'Attendee ID_2'], keep='first')\
         .merge(df_att, on='Attendee ID')\
         .merge(df_att, left_on='Attendee ID_2', right_on='Attendee ID', suffixes=['', '_2'])\
         .rename(columns={'Attendee_2' : 'Contact', 'Contact_Type' : 'Contact Type'})

df_all.drop(columns=[c for c in df_all.columns if 'ID' in c], inplace=True)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_all.to_csv(r'.\outputs\output-2021-45.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['TC Output.csv']
my_files = ['output-2021-45.csv']
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
