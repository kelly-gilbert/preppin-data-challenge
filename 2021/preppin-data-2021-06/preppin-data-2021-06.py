# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2021-06
https://preppindata.blogspot.com/2021/02/2021-week-6-comparing-prize-money-for.html
 
Comparing Prize Money for Professional Golfers

- Input the data
- Answer these questions:
    - What's the Total Prize Money earned by players for each tour?
    - How many players are in this dataset for each tour?
    - How many events in total did players participate in for each tour?
    - How much do players win per event? What's the average of this for each tour?
    - How do players rank by prize money for each tour? What about overall? 
      What is the average difference between where they are ranked within their tour compared to 
      the overall rankings where both tours are combined?
      Here we would like the difference to be positive as you would presume combining the tours 
      would cause a player's ranking to increase
- Combine the answers to these questions into one dataset
- Pivot the data so that we have a column for each tour, with each row representing an answer to 
  the above questions
- Clean up the Measure field and create a new column showing the difference between the tours for 
  each measure
  We're looking at the difference between the LPGA from the PGA, so in most instances this number 
  will be negative
- Output the data

Author: Kelly Gilbert
Created: 2021-02-10
Requirements: 
  - input dataset (PGALPGAMoney2019.xlsx)
  - output dataset (for results check):
    - 2021W06 Output.csv
  
"""


from pandas import ExcelFile, melt, merge

# used for answer check
from pandas import read_csv


# import the data from all sheets and create the Store column
xl = ExcelFile(r'.\inputs\PGALPGAMoney2019.xlsx')
df = xl.parse(0)
df.info()

# calculate the avg prize money per event, by person
# note, the solution takes an average of this average, and not a weighted average
df['avg_money_by_person'] = df['MONEY'] / df['EVENTS']

# aggregate by tour
dfAgg = df.groupby('TOUR').agg(Total_Prize_Money = ('MONEY', 'sum'),
                                 Number_of_Players = ('PLAYER NAME', 'count'),
                                 Number_of_Events = ('EVENTS', 'sum'),
                                 Avg_Money_per_Event = ('avg_money_by_person', 'mean')).reset_index()
dfAgg['Avg_Money_per_Event'] = dfAgg['Avg_Money_per_Event'].round(0).astype(int)

# rank
df['overall_rank'] = df['MONEY'].rank(method='first', ascending=False)
df['tour_rank'] = df.groupby('TOUR')['MONEY'].rank(method='first', ascending=False)
df['rank_diff'] = df['overall_rank'] - df['tour_rank']

dfRankAgg = df.groupby('TOUR').agg(Avg_Difference_in_Ranking = ('rank_diff', 'mean')).reset_index()

# join the dataframes
dfAll = dfAgg.merge(dfRankAgg, how='left', on='TOUR')

# melt fieldnames into rows
dfAll = melt(dfAll, id_vars = ['TOUR'])

# pivot tour into cols
dfAll = dfAll.pivot(index='variable', columns='TOUR', values='value').reset_index()
dfAll['Difference between tours'] = dfAll['LPGA'] - dfAll['PGA']

# rename cols and remove underscores from measure names
dfAll.rename( columns = { 'variable' : 'Measure'}, inplace=True)
dfAll['Measure'] = dfAll['Measure'].str.replace('_', ' ')

# output
dfAll.to_csv('.\\outputs\\output-2021-06.csv', index=False)


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solution_files = ['2021W06 Output.csv']
my_files = ['output-2021-06.csv']
col_order_matters = False

for i in range(len(solution_files)):
    print('---------- Checking \'' + solution_files[i] + '\' ----------\n')
    
    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_files[i])
    df_mine = read_csv('.\\outputs\\' + my_files[i])
    
    # are the fields the same and in the same order?
    solution_cols = list(df_solution.columns)
    my_cols = list(df_mine.columns)
    if col_order_matters == False:
         solution_cols.sort()
         my_cols.sort()

    col_match = False
    if solution_cols != my_cols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_solution.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
    else:
        print('Columns match\n')
        col_match = True
    
    # are the values the same? (only check if the columns matched)
    if col_match == True:
        df_solution['check'] = 1
        df_mine['check'] = 1
        df_compare = df_solution.merge(df_mine, how='outer', on=list(df_solution.columns)[:-1])
        
        if df_compare['check_x'].count() != len(df_compare):
            print('*** Values do not match ***')
            print(df_compare[df_compare['check_x'] != df_compare['check_x']])
        else:
            print('Values match')
    
    print('\n')
    
    df_mine['Difference between tours'] == df_solution['Difference between tours']