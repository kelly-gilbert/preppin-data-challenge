# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 49 Departmental December Human Resources
https://preppindata.blogspot.com/2021/12/2021-week-49-departmental-december.html

- Input data
- Create the Employment Range field which captures the employees full tenure at the company in the 
  MMM yyyy to MMM yyyy format. 
- Work out for each year employed per person:
    - Number of months they worked
    - Their salary they will have received 
    - Their sales total for the year
- For each Reporting Year (the individual year someone worked for us), calculate their cumulative months (called Tenure)
- Determine the bonus payments the person will have received each year
    - It's 5% of their sales total
- Round Salary Paid and Yearly Bonus to two decimal places 
- Add Salary Paid and Yearly Bonus together to form Total Paid
- Output the data

Author: Kelly Gilbert
Created: 2021-12-08
Requirements:
  - input dataset:
      - PD 2021 Wk 49 Input - Input.csv
  - output dataset (for results check only):
      - PD 2021 Wk 49 Output.csv
"""


from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = read_csv(r'.\\inputs\\PD 2021 Wk 49 Input - Input.csv', parse_dates=['Date'], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# add the reporting year
df['Reporting Year'] = df['Date'].dt.year


# summarize by person and year
df_out = df.groupby(['Name', 'Reporting Year']).agg(min_date=('Date', 'min'),
                                                    max_date=('Date', 'max'),
                                                    months_worked=('Date', 'count'),
                                                    annual_salary=('Annual Salary', 'mean'),
                                                    total_sales=('Sales', 'sum')).reset_index()


# calculate salary and bonus
df_out['Salary Paid'] = (df_out['annual_salary'] / 12 * df_out['months_worked']).round(2)
df_out['Yearly Bonus'] = (df_out['total_sales'] * 0.05).round(2)
df_out['Total Paid'] = (df_out['Salary Paid'] + df_out['Yearly Bonus']).round(0)


# calculate cumulative tenure
df_out['Tenure by End of Reporting Year'] = df_out.groupby('Name')['months_worked'].cumsum()

    
# create the Employment Range field which captures the employees full tenure at the company                         
df_out['Employment Range'] = df_out.groupby(['Name'])['min_date'].transform('min').dt.strftime('%b %Y') \
                             + ' to ' \
                             + df_out.groupby(['Name'])['max_date'].transform('max').dt.strftime('%b %Y')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.rename(columns={'annual_salary' : 'Annual Salary'})

cols = ['Name', 'Employment Range', 'Reporting Year', 'Tenure by End of Reporting Year', 
        'Salary Paid', 'Yearly Bonus', 'Total Paid']
df_out.to_csv(r'.\outputs\output-2021-49.csv', index=False, columns=cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 49 Output.csv']
my_files = ['output-2021-49.csv']
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
    