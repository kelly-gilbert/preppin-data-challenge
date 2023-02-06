# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 52 - Find Sub-Departments from an employee hierarchy (HR Month)
https://preppindata.blogspot.com/2022/12/2022-week-52-find-sub-departments-from.html

- Input the data
- From the employee data, calculate each person’s hierarchy_level
  - The employee_id_hierarchy field contains a person’s supervisory hierarchy flattened into a string 
    (e.g. | CEO’s ID | Vice President’s ID | Director’s ID | Manager’s ID | Employee’s ID |)
  - To calculate the hierarchy level, count the number of pipes (|) in the employee_id_hierarchy 
    and subtract 1
- Identify the sub-department heads
  - Exclude any employees in the “Executives” department
  - Exclude any employees with “Administrator” in their title
  - Find the person with the 2nd-lowest hierarchy_level within each department – those people are 
    the sub-department heads
- Parse out the dependent_team_ids for the sub-department heads –> those are the sub-department 
  team IDs. Rename the field subdept_team_id.
- Join the sub-departments back to the main employee data
  - An employee is in the sub-department if
    - The employee’s team hierarchy string contains the subdept_team_id
    - OR, the employee’s dependent_team_ids contains the subdept_team_id
- Join the subdept_team_id to the team lookup list, to get the sub-department name. Rename the
  column subdept_name.
- Make sure that all employees are included in the output, even if they do not have a sub-department
  (e.g. the CEO). If an employee doesn’t have a sub-department, the sub-department fields should be null.
- Output the data 

Author: Kelly Gilbert
Created: 2023-02-05
Requirements:
  - input dataset:
      - employees.xlsx
  - output dataset (for results check only):
      - employees_with_subdept.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution
from numpy import nan


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\employees.xlsx') as xl:
    df_ee = pd.read_excel(r'.\inputs\employees.xlsx', sheet_name='Employees') 
    df_team = pd.read_excel(r'.\inputs\employees.xlsx', sheet_name='Teams')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# find the hierarchy level
df_ee['hierarchy_level'] = df_ee['employee_id_hierarchy'].str.count('\|') - 1


# find the sub-departments
df_ee['hierarchy_rank'] = df_ee.groupby('department')['hierarchy_level'].rank(method='dense')

df_subd = ( df_ee.query("department != 'Executives'" 
                   + " & not title.str.contains('Administrator')"
                   + " & hierarchy_rank == 2""")
              [['employee_id', 'department', 'dependent_team_ids']]
              .assign(subdept_team_id = lambda df_x: df_x['dependent_team_ids'].str.split('|'))
              .explode('subdept_team_id')
              .query("subdept_team_id != ''") )


# find the subdepartment for each employee
# the employee is in the subdepartment if the subdepartment_team_id is present in either the
#    team_hierarchy or the dependent_team_ids
df_ee_subd = ( df_ee[['employee_id', 'position_id', 'department', 'team_hierarchy', 
                      'dependent_team_ids']]
                    .merge(df_subd, 
                           on='department', 
                           how='inner', 
                           suffixes=['','_subd'])
                    .assign(subdept_team_id = lambda df_x: 
                                [s 
                                 if s in th or (dt == dt and s in dt) 
                                 else nan
                                 for th, dt, s 
                                 in zip(df_x['team_hierarchy'], 
                                        df_x['dependent_team_ids'],
                                        df_x['subdept_team_id'])] )
                    .query('subdept_team_id == subdept_team_id') )


# join to the main employee list an add the subdept name
df_out = ( df_ee.merge(df_ee_subd[['employee_id', 'position_id', 'subdept_team_id']],
                       on=['employee_id', 'position_id'],
                       how='left')
                .merge(df_team.rename(columns={'team_id' : 'subdept_team_id', 
                                                'team_name' : 'subdept_name'}),
                       on='subdept_team_id',
                       how='left')
                .drop(columns='hierarchy_rank') )
              
              
#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-52.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\employees_with_subdept.csv']
my_files = [r'.\outputs\output-2022-52.csv']
unique_cols = [['employee_id', 'position_id']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)


#---------------------------------------------------------------------------------------------------
# performance testing
#---------------------------------------------------------------------------------------------------

%%timeit
# using query
test = df_ee_subd.query('subdept_team_id.notna()')


%%timeit
# using loc indexing
test = df_ee_subd.loc[df_ee_subd['subdept_team_id'].notna()] 
