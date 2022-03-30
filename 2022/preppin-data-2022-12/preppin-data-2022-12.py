# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 12 - Gender Pay Gap
https://preppindata.blogspot.com/2022/03/2022-week-12-gender-pay-gap.html

- Input the data
- Combine the files
- Keep only relevant fields
- Extract the Report years from the file paths
- Create a Year field based on the the first year in the Report name
- Some companies have changed names over the years. For each EmployerId, find the most recent report
  they submitted and apply this EmployerName across all reports they've submitted
- Create a Pay Gap field to explain the pay gap in plain English
    - You may encounter floating point inaccuracies. Find out more about how to resolve them here
    - In this dataset, a positive DiffMedianHourlyPercent means the women's pay is lower than the 
      men's pay, whilst a negative value indicates the other way around
    - The phrasing should be as follows:
        - In this organisation, women's median hourly pay is X% higher/lower than men's.
        - In this organisation, men's and women's median hourly pay is equal.
- Output the data

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input dataset:
      - 
  - output dataset (for results check only):
      - Pay Gap Output.csv
"""

from numpy import nan, where
from os import listdir, path
import pandas as pd


IN_DIR = r'.\inputs'


#---------------------------------------------------------------------------------------------------
# input the data and add the Report and Year fields
#---------------------------------------------------------------------------------------------------

usecols = ['EmployerName', 'EmployerId', 'EmployerSize', 'DiffMedianHourlyPercent', 'DateSubmitted']

df = pd.concat([pd.read_csv(path.join(IN_DIR, f), encoding='utf-8', usecols=usecols)\
                  .assign(Report=f[-16:-4],
                          Year=int(f[-16:-12])) 
                for f in listdir(IN_DIR)], ignore_index=True)
    

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# fill in missing submission dates
df['DateSubmitted'] = where(df['DateSubmitted'].notna(), 
                            pd.to_datetime(df['DateSubmitted']), 
                            pd.to_datetime(df['Year'].astype(str) + '-01-01'))


# get the most recent EmployerName   
df = df.sort_values(by=['EmployerId', 'DateSubmitted'], ascending=False)\
       .assign(EmployerName=lambda df_x: where(df_x['EmployerId'].shift(1) != df_x['EmployerId'], 
                                    df_x['EmployerName'], nan))\
       .assign(EmployerName=lambda df_x: df_x.groupby('EmployerId')['EmployerName'].ffill())\
       .reset_index(drop=True)


# create the pay gap field
df['gap_fmt'] = df['DiffMedianHourlyPercent'].round(2).abs()\
                    .astype(str).str.replace('\.?0$', '', regex=True)
df['Pay Gap'] = pd.Series(
                    where(df['DiffMedianHourlyPercent'] == 0, 
                          "In this organisation, men's and women's median hourly pay is equal.",
                          "In this organisation, women's median hourly pay is " + df['gap_fmt'] + \
                              where(df['DiffMedianHourlyPercent'] > 0, "% lower ", "% higher ") + \
                              "than men's."))

    
#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['DiffMedianHourlyPercent', 'EmployerId', 'EmployerName', 'EmployerSize', 'Pay Gap',
            'Report', 'Year']
df.to_csv(r'.\outputs\output-2022-12.csv', index=False, columns=out_cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Pay Gap Output.csv']
my_files = ['output-2022-12.csv']
unique_cols = [['EmployerId', 'Year', 'EmployerSize']]
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
            print('\n\n*** Missing or extra records ***')
            print('\n\nIn solution, not in mine:\n')
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
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])
                                   & ((df_compare[f'{c}_sol'].notna()) 
                                      | (df_compare[f'{c}_mine'].notna()))]

            if len(unmatched) > 0:
                print(f'\n\n*** Values do not match: {c} ***\n')
                print(unmatched[unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                errors += 1
        
        if errors == 0:
            print('Values match')

    print('\n')  


#---------------------------------------------------------------------------------------------------
# performance profiling - getting the most recent EmployerName
#---------------------------------------------------------------------------------------------------

# method 1 - sort and drop duplicates, merge back to main df
# input dataset: 35.5 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 15: 476 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 30: 895 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
%%timeit -n 10 -r 1
latest_name = df[['DateSubmitted', 'EmployerId', 'EmployerName']].sort_values(by='DateSubmitted')\
                  .drop_duplicates('EmployerId', keep='last')\
                  .drop(columns='DateSubmitted')\
                  .set_index('EmployerId')
df2 = df.merge(latest_name, on='EmployerId', how='inner', suffixes=['_old', ''])\
        .drop(columns='EmployerName_old')


# method 2 - sort & join, except use indexing instead of drop duplictes -- MUCH SLOWER than #1
# input dataset: 629 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 15: 4.29 s ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 30: 26.6 s ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
%%timeit -n 10 -r 1
latest_name = df.loc[df.groupby('EmployerId')['DateSubmitted'].idxmax()][['EmployerId', 'EmployerName']]
df2 = df.merge(latest_name, on='EmployerId', how='inner', suffixes=['_old', ''])\
        .drop(columns='EmployerName_old')


# method 3 - sort and fill down -- slightly faster than #1
# input dataset: 35.5 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 15: 402 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 30: 813 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
%%timeit -n 10 -r 1
df2 = df.sort_values(by=['EmployerId', 'DateSubmitted'], ascending=False)\
        .assign(EmployerName2=lambda df_x: where(df_x['EmployerId'].shift(1) != df_x['EmployerId'], 
                                     df_x['EmployerName'], nan))\
        .assign(EmployerName2=lambda df_x: df_x.groupby('EmployerId')['EmployerName2'].ffill())


# method 4 - groupby + idxmax + merge -- SLOW
# input dataset: 629 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 15: 1.02 s ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 30: 1.43 s ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
%%timeit -n 10 -r 1
latest_name = df.set_index('EmployerName')\
                .groupby('EmployerId').agg(EmployerName=('DateSubmitted', 'idxmax'))
df2 = df.merge(latest_name, on='EmployerId', how='inner', suffixes=['_old', ''])\
        .drop(columns='EmployerName_old')


# method 5 - groupby + transform -- SLOW
# input dataset: 602 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# input dataset x 15: 719 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
# 840 ms ± 0 ns per loop (mean ± std. dev. of 1 run, 10 loops each)
%%timeit -n 10 -r 1
df2 = df.set_index('EmployerName')\
        .assign(EmployerName=lambda df_x: df_x.groupby('EmployerId')['DateSubmitted'].transform('idxmax'))


# increase the size of the dataset
# df = pd.concat([df for i in range(0,15)])
# df = pd.concat([df for i in range(0,2)])


# plots
df_timeit = pd.DataFrame({'method' : [1, 2, 3, 4, 5] * 3,
                          'record_count' : [41276] * 5 + [41276 * 15] * 5 + [41276 * 30] * 5,
                          'run_time_ms' : [35.5, 629, 35.5, 629, 602] \
                                          + [476, 4290, 402, 1020, 719] \
                                          + [895, 26660, 813, 1430, 840]})

df_timeit_p = df_timeit.pivot(index='record_count', columns='method', values='run_time_ms')

# plot all methods by record count
colors = ['blue', 'orange', 'green', 'red', 'purple']
df_timeit_p.plot.line(title='Mean Run Time by Dataset Size',
                      xlabel='Record Count', ylabel='Time (ms)', color=colors)

# plot without method 2
df_timeit_p.drop(columns=2)\
           .plot.line(title='Mean Run Time by Dataset Size', 
                      xlabel='Record Count', ylabel='Time (ms)', color=[colors[0]] + colors[2:])
