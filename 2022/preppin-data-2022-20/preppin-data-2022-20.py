# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 20 - TC22 Session Attendance
https://preppindata.blogspot.com/2022/05/2022-week-20-tc22-session-attendance.html

- Input the data
- In the Registrations Input, tidy up the Online/In Person field
- From the Email field, extract the company name (hint)
  - We define the company name as being the text following the @ symbol, up to the .
- Count the number of sessions each registered person is planning to attend
- Join on the Session Lookup table to replace the Session ID with the Session name
- Join the In Person Attendees dataset to the cleaned Registrations
  - You will need multiple join clauses
  - Think about the Join Type, we only want to return the names of those that did not attend the 
    sessions they registered for
- Filter to only include those who registered to be In Person
- Join the Online Attendees dataset to the cleaned Registrations
  - You will need multiple join clauses
  - Think about the Join Type, we only want to return the names of those that did not attend the 
    sessions they registered for
- Filter to only include those who registered to be Online
- Union together these separate streams to get a complete list of those who were unable to attend 
  the sessions they registered for
- Count the number of sessions each person was unable to attend
- Calculate the % of sessions each person was unable to attend
  - Round this to 2 decimal places
- Remove unnecessary fields 
- Output the data

Author: Kelly Gilbert
Created: 2022-07-04
Requirements:
  - input dataset:
      - TC22 Input.xlsx 
  - output dataset (for results check only):
      - TC22 Output.csv
"""


import pandas as pd
from numpy import where
import output_check  # custom module for comparing output to the solution file


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\TC22 Input.xlsx') as xl:
    df_reg = pd.read_excel(xl, sheet_name='Registrations')
    df_ses = pd.read_excel(xl, sheet_name='Sessions')
    df_online = pd.read_excel(xl, sheet_name='Online Attendees')
    df_inp = pd.read_excel(xl, sheet_name='In Person Attendees')
            

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# tidy up the online/in person field
#df_reg['Online/In Person'].unique()
df_reg['Online/In Person'] = where(df_reg['Online/In Person'].str.lower().str[0]=='o',
                                   'Online', 'In Person')
    

# look up the session name
df_reg['Session'] = df_reg['Session ID'].replace(dict(zip(df_ses['Session ID'], df_ses['Session'])))


# total registered sessions by person
df_reg['Registered_Count'] = df_reg.groupby('Email')['Session'].transform('count')


# join the attendance data to the registration data
df_reg_onl = df_reg[df_reg['Online/In Person']=='Online']
df_reg_inp = df_reg[df_reg['Online/In Person']=='In Person']
df_online['Attended'] = 1
df_inp['Attended'] = 1

df_combined = pd.concat( 
    [df_reg_onl.merge(df_online, on=['Email', 'Session'], how='left'),
     df_reg_inp.merge(df_inp, on=['First Name', 'Last Name', 'Session'], how='left')]
)


# calculate % not attended and output the sessions not attended
df_out = ( df_combined.loc[df_combined['Attended'].isna()]
               .rename(columns={'Session' : 'Session not attended'}) )
df_out['Not Attended %'] = (df_out.groupby('Email')['Session not attended'].transform('count') 
                            / df_out['Registered_Count'] * 100).round(2)


# from the Email field, extract the company name (text between @ and .)
df_out['Company'] = df_out['Email'].str.extract('.*@(.*?)\..*')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-20.csv', index=False, 
              columns=['Company', 'First Name', 'Last Name', 'Email', 'Online/In Person', 
                       'Session not attended', 'Not Attended %'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\TC22 Output.csv']
my_files = [r'.\outputs\output-2022-20.csv']
unique_cols = [['Company', 'First Name', 'Last Name', 'Email', 'Online/In Person', 
                'Session not attended']]
col_order_matters = True
round_dec = 8

output_check.output_check(solution_files, my_files, unique_cols, col_order_matters = False)


#---------------------------------------------------------------------------------------------------
# options for joining attendance to registrations
#---------------------------------------------------------------------------------------------------

# # option 1 = join online to main, then join in-person to that result
# 1.34 s ± 125 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) (duplicating df_reg 100x)

%%timeit 
df_online['Online/In Person'] = 'Online'
df_online['Attended'] = 1
df_inp['Online/In Person'] = 'In Person'
df_inp['Attended'] = 1

df_combined_1 = ( 
    df_reg.merge(df_online, on=['Email', 'Online/In Person', 'Session'], how='left')
          .merge(df_inp, on=['First Name', 'Last Name', 'Online/In Person', 'Session'], how='left')
)


# option 2 = split main into online and in-person; join each part to the appropriate attendee list;
#            concatenate the result -- FASTEST
# 1.13 s ± 76.7 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) (duplicating df_reg 100x)

%%timeit 
df_reg_onl = df_reg[df_reg['Online/In Person']=='Online']
df_reg_inp = df_reg[df_reg['Online/In Person']=='In Person']
df_online['Attended'] = 1
df_inp['Attended'] = 1

df_combined_2 = pd.concat( 
    [df_reg_onl.merge(df_online, on=['Email', 'Session'], how='left'),
      df_reg_inp.merge(df_inp, on=['First Name', 'Last Name', 'Session'], how='left')]
)


# option 3 = replace name with email in in-person attendees; concat online and in-person lists;
#            concatenate and join to main table
# 2.5 s ± 201 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) (duplicating df_reg 100x)

%%timeit 
df_online['Online/In Person'] = 'Online'
df_inp['Online/In Person'] = 'In Person'
df_emails = df_reg.groupby(['First Name', 'Last Name'], as_index=False)['Email'].max()

df_inp['Email'] = ( (df_inp['First Name'] + ' ' + df_inp['Last Name'])\
                        .replace(dict(zip(df_emails['First Name'] + ' ' + df_emails['Last Name'], 
                                          df_emails['Email']))) )

df_combined_3 = df_reg.merge(pd.concat([df_online, df_inp]).assign(Attended=1), 
                             on=['Email', 'Online/In Person', 'Session'], how='left')


#---------------------------------------------------------------------------------------------------
# options for calculating % attended
#--------------------------------------------------------------------------------------------------

# option 1: calculate Not Attended % by person, join to not attended list -- FASTER
# 2.15 s ± 111 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) (duplicating df_reg 1000x)

%%timeit 
df_sum = df_combined.groupby('Email', as_index=False).agg(Reg_Count=('Session', 'count'),
                                                          Attended_Count=('Attended', 'sum'))
df_sum['Not Attended %'] = ((1 - df_sum['Attended_Count'] / df_sum['Reg_Count']) * 100).round(2)

df_out = df_combined[df_combined['Attended'].isna()].merge(df_sum, on='Email')


# option 2: transform not attended % by person, filter list to not attended -- FASTEST
# 2.82 s ± 67.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) (duplicating df_reg 1000x)

%%timeit 
df_combined['Attended_Count'] = df_combined.groupby('Email')['Attended'].transform('sum')
df_combined['Reg_Count'] = df_combined.groupby('Email')['Session'].transform('count')

df_out = df_combined.loc[df_combined['Attended'].isna()]
df_out['Not Attended %'] = ((1 - df_out['Attended_Count'] / df_out['Reg_Count']) * 100).round(2)


# option 3: calc total sessions in main dataset, calculate % on subset
# 1.7 s ± 14.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) (duplicating df_reg 1000x)
%%timeit 
df_combined['Reg_Count'] = df_combined.groupby('Email')['Session'].transform('count')

df_out = df_combined.loc[df_combined['Attended'].isna()]
df_out['Not Attended %'] = ((1 - df_out.groupby('Email')['Session'].transform('count') 
                                 / df_out['Reg_Count']) * 100).round(2)
