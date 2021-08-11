# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 28 - It's Coming Rome
https://preppindata.blogspot.com/2021/07/2021-week-28-its-coming-rome.html

- Input Data
- Determine what competition each penalty was taken in
- Clean any fields, correctly format the date the penalty was taken, & group the two German 
  countries (eg, West Germany & Germany)
- Rank the countries on the following: 
  - Shootout win % (exclude teams who have never won a shootout)
  - Penalties scored %
  - What is the most and least successful time to take a penalty? (What penalty number are you most
    likely to score or miss?)
- Output the Data

Author: Kelly Gilbert
Created: 2021-08-11
Requirements:
  - input dataset:
      - InternationalPenalties.xlsx
  - output dataset (for results check only):
      - Week 28 Output.xlsx
"""


from numpy import where
from pandas import concat, ExcelFile, ExcelWriter, read_excel, Series, to_datetime


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = None
with ExcelFile(r'.\\inputs\\InternationalPenalties.xlsx') as xl:
    for s in xl.sheet_names:
        df_temp = read_excel(xl, s)
        df_temp.columns = [c.lower().strip() for c in df_temp.columns]
        df_temp['sheet'] = s
        df = concat([df, df_temp])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# melt winner/loser into rows
df_m = df.melt(id_vars=[c for c in df.columns if c not in (['winner', 'loser'])],
               value_vars=['winner', 'loser'], value_name='Team')


# clean team name
df_m['Team'] = df_m['Team'].str.replace('.*Germany.*', 'Germany').str.strip()


# update date with year (note, this field isn't used in the output, but this in the requirements)
df_m['date'] = to_datetime(df_m['event year'].str[0:4] + df_m['date'].dt.strftime('-%m-%d'))


# add counters for summarization
df_m['shootout_id'] = df_m['sheet'] + '|' + df_m['no.'].astype(str)
df_m['penalty_scored_flag'] = Series(where(df_m['variable'] == 'winner',
                                           df_m['winning team taker'],
                                           df_m['losing team taker']))\
                              .str.lower().str.contains('penalty scored')
df_m['winner_flag'] = where((df_m['variable'] == 'winner') & (df_m['penalty number'] == 1), 1, 0)


# output 1: shootout win %
out1 = df_m.groupby('Team').agg(Total_Shootouts=('shootout_id', 'nunique'),
                                Shootouts=('winner_flag', 'sum'))\
                           .reset_index()
out1.columns = [c.replace('_', ' ') for c in out1.columns]
out1['Shootout Win %'] = round(out1['Shootouts'] / out1['Total Shootouts'] * 100, 0)
out1['Win % Rank'] = out1['Shootout Win %'].rank(method='dense', ascending=False).astype(int)
out1 = out1.loc[out1['Shootouts'] > 0]


# output 2: penalties scored %
out2 = df_m.groupby('Team').agg(Total_Penalties=('penalty_scored_flag', 'count'),
                                Penalties_Scored=('penalty_scored_flag', 'sum'))\
                           .reset_index()
out2.columns = [c.replace('_', ' ') for c in out2.columns]
out2['Penalties Missed'] = out2['Total Penalties'] - out2['Penalties Scored']
out2['% Total Penalties Scored'] = round(out2['Penalties Scored'] /
                                         out2['Total Penalties'] * 100, 0)
out2['Penalties Scored %Rank'] = out2['% Total Penalties Scored']\
                                    .rank(method='dense', ascending=False).astype(int)


# output 3: penalties score % by position
out3 = df_m.groupby('penalty number').agg(Total_Penalties=('penalty_scored_flag', 'count'),
                                Penalties_Scored=('penalty_scored_flag', 'sum'))\
                           .reset_index()
out3.columns = [c.replace('_', ' ').title() for c in out3.columns]
out3['Penalties Missed'] = out3['Total Penalties'] - out3['Penalties Scored']
out3['Penalty Scored %'] = round(out3['Penalties Scored'] /
                                 out3['Total Penalties'] * 100, 0)
out3['Rank'] = out3['Penalty Scored %'].rank(method='dense', ascending=False).astype(int)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

with ExcelWriter(r'.\outputs\output-2021-28.xlsx') as w:
    out1[['Win % Rank', 'Shootout Win %', 'Total Shootouts', 'Shootouts', 'Team']]\
        .to_excel(w, sheet_name='Win %', index=False)

    out2[['Penalties Scored %Rank', '% Total Penalties Scored', 'Penalties Missed',
          'Penalties Scored', 'Team']]\
        .to_excel(w, sheet_name='Score %', index=False)

    out3[['Rank', 'Penalty Scored %', 'Penalties Scored', 'Penalties Missed', 'Total Penalties',
          'Penalty Number']]\
        .to_excel(w, sheet_name='Penalty Position', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Week 28 Output.xlsx']
my_files = ['output-2021-28.xlsx']
col_order_matters = False


for i, solution_file in enumerate(solution_files):
    xl_solution = ExcelFile('.\\outputs\\' + solution_file)
    xl_mine = ExcelFile('.\\outputs\\' + my_files[i])

    for s in xl_solution.sheet_names:

        print('---------- Checking \'' + solution_file + '\', sheet \'' + s + '\' ----------\n')

        # read in the files
        df_solution = read_excel(xl_solution, s)
        df_mine = read_excel(xl_mine, s)

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
