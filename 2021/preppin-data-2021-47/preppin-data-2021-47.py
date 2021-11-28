# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 47 - Games Night Viz Collab
https://preppindata.blogspot.com/2021/11/2021-week-47-games-night-viz-collab.html

- Input the Data
- Add the player names to their poker events
- Create a column to count when the player finished 1st in an event
- Replace any nulls in prize_usd with zero
- Find the dates of the players first and last events
- Use these dates to calculate the length of poker career in years (with decimals)
- Create an aggregated view to find the following player stats:
- Number of events they've taken part in
  - Total prize money
  - Their biggest win
  - The percentage of events they've won
  - The distinct count of the country played in
  - Their length of career
- Reduce the data to name, number of events, total prize money, biggest win, percentage won, 
  countries visited, career length
  
Creating a Pizza Plot / Coxcomb chart output:
- Using the player stats to create two pivot tables
  -  a pivot of the raw values
  -  a pivot of the values ranked from 1-100, with 100 representing the highest value
- Note: we're using a ranking method that averages ties, pay particular attention to 
  countries visited!
- Join the pivots together
- Output the data (4 fields)
  - name
  - metric
  - raw_value
  - scaled_value

Author: Kelly Gilbert
Created: 2021-11-25
Requirements:
  - input dataset:
      - top_female_poker_players_and_events.xlsx
  - output dataset (for results check only):
      - output.csv
"""


import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from numpy import ceil, pi, where
from pandas import ExcelFile, melt, read_excel
from textwrap import wrap

# for results check only:
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\top_female_poker_players_and_events.xlsx') as xl:
    df_p = read_excel(xl, 'top_100')
    df_e = read_excel(xl, 'top_100_poker_events')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# replace any nulls in prize_usd with zero
df_e['prize_usd'] = df_e['prize_usd'].fillna(0)


# summarize event metrics for each player and add the player name
df_e['first_place'] = where(df_e['player_place']=='1st', 1, 0)
df_p_tot = df_e.groupby('player_id').agg(wins=('first_place', 'sum'),
                                         number_of_events=('event_date', 'count'),
                                         first_event=('event_date', 'min'),
                                         last_event=('event_date', 'max'),
                                         biggest_win=('prize_usd', 'max'),
                                         countries_visited=('event_country', 'nunique'))\
               .reset_index()\
               .merge(df_p[['player_id', 'name', 'all_time_money_usd']], on='player_id', how='left')\
               .rename(columns={'all_time_money_usd' : 'total_prize_money'})


# calculate win % and career length
df_p_tot['percent_won'] = df_p_tot['wins'] / df_p_tot['number_of_events']
df_p_tot['career_length'] = ((df_p_tot['last_event'] - df_p_tot['first_event']).dt.days) / 365.25


# pivot the metrics into rows
metrics = ['number_of_events', 'total_prize_money', 'biggest_win', 'percent_won', 
           'countries_visited', 'career_length']
df_out = df_p_tot.melt(id_vars='name', value_vars=metrics, var_name='metric', value_name='raw_value')
df_out['scaled_value'] = df_out.groupby('metric')['raw_value'].rank(method='average', ascending=True)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2021-47.csv', index=False)


#---------------------------------------------------------------------------------------------------
# radial bar chart
#---------------------------------------------------------------------------------------------------

# NOTE: this is not a good chart choice for this use case. I've recreated the chart here for my
# own practice (to see if I could figure it out!) but would not use this in practice.
#
#   The questions a user might be asking of this data are:
#   1 - Who are the top players across all metrics?
#   2 - Who are the top players for each individual metric (e.g. who had the highest win %?)
#   3 - I'm interested in player X. How did she perform across different metrics?
#
#   All of these questions are difficult to answer. It's possibly easiest to answer #3, but it's 
#   hard to tell the scale (is her red pie slice at 50 or 100?) This could be corrected by adding a 
#   100% circle around each chart.
#   A user could potentially answer #2 by scanning for larger areas, but it's very difficult to 
#   compare across players
#
#   Also, since the metrics are scaled by rank, there isn't a sense of scale across players (e.g. 
#   Is there a big gap between first and 2nd place?)
# 
#   Some better choices:
#   A bump chart would help us answer all three questions (keeping the scaled rank), although
#     interactivity may be needed to help a user find a specific player for #3.
#   A parallel coordinates chart would help answer 1 and 2 (adding interactivity where a user could
#     highlight a specific player would cover #3).
#   Bar charts by metric would help us answer #2, and potentially #1 if the top players in each
#     metric are similar. We could also eliminate the rank scale to show meaningful differences.
#     Highlight interaction would help answer #3.   



# I used these examples while creating the chart output:
# Circular barplot: https://www.python-graph-gallery.com/circular-barplot-basic
# Small multiples: https://jonathansoma.com/lede/data-studio/classes/small-multiples/long-explanation-of-using-plt-subplots-to-create-small-multiples/


# dimensions of the chart grid
player_count = df_out['name'].nunique()
metric_count = df_out['metric'].nunique()
CHARTS_PER_ROW = 7    # number of horizontal charts
CHARTS_PER_COL = int(ceil(player_count / CHARTS_PER_ROW))


# assign colors to each metric name
color_map = { 'biggest_win' : '#a9ded5',        # green
              'career_length' : '#ffffc5',      # yellow
              'countries_visited' : '#cecbe3',  # purple
              'number_of_events' : '#fc9f94',   # red
              'percent_won' : '#9fc4de',        # blue
              'total_prize_money' : '#fdc688'}  # orange


# calculate the width and central angle for each bar, in radians
# the original chart starts with biggest_win at 180 degrees, then moves clockwise, alphabetically
width = 2*pi / metric_count
df_out['angle'] = pi + (2*pi - (df_out['metric'].rank(method='dense') - 1) * 2*pi / metric_count) 


# initialize as polar coordinates and get all of the subplot axes
fig, axes = plt.subplots(figsize=(CHARTS_PER_ROW * 2.1, CHARTS_PER_COL * 2), 
                         subplot_kw={"projection": "polar"}, 
                         nrows=CHARTS_PER_COL, ncols=CHARTS_PER_ROW, sharex=True, sharey=True)

# flatten the axis list
#     axes is a list of lists (each element in axes is a row of axes, 
#     and each element of the row is an axis)
axis_list = [ax for row in axes for ax in row]


# make axis 0 blank and float a legend over it
ax = axis_list[0]
ax.axis('off')   

handles = [mpatches.Patch(color=v, label=k) for k, v in color_map.items()]
fig.legend(handles=handles, bbox_to_anchor=(0.14, 0.985), frameon=False)
    # bbox is relative to the whole size of the outer figure (where 1,1 is the upper right corner)
    # and position is the middle of the legend

# edit the subplot axes
n = 1
for player_name, player_data in df_out.groupby(['name']):

    # get the current axis
    ax = axis_list[n]
    
    # draw the radial bars
    ax.bar(
        x=player_data['angle'], 
        height=player_data['scaled_value'], 
        width=width, 
        bottom=0, 
        linewidth=1, 
        edgecolor='darkgray',
        color=player_data['metric'].map(color_map)
    )    
    
    # add title, format player chart
    ax.set_title("\n".join(wrap(player_name, 15, break_long_words=False)), y=-0.6) 
    ax.set_ylim(0, 100)    
    ax.axis('off')                     # remove the axis labels/grid
 
    n += 1


# remove extra axes (if CHARTS_PER_COL * CHARTS_PER_ROW > player_count)
for ax in axis_list[player_count+1:]:
    ax.remove()
    
    
# overall title
plt.suptitle('Top 100 Female Poker Players', fontsize=22, fontweight=4, y=1.02)

# overall layout adjustments
plt.tight_layout()
plt.subplots_adjust(wspace = 1.25, hspace = 1.25)  

plt.show()


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['output.csv']
my_files = ['output-2021-47.csv']
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
