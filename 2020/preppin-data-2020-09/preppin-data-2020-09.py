# -*- coding: utf-8 -*-
"""
Preppin' Data 2020: Week 9 - C&BS Co: Political Monitoring
https://preppindata.blogspot.com/2020/02/2020-week-9.html

- Input data
- Remove the Average Record for the polls
- Clean up your Dates
- Remove any Null Poll Results
- Form a Rank (modified competition) of the candidates per Poll based on their results
- Determine the spread for each poll from 1st Place to 2nd Place
- Rename Sample Types: RV = Registered Voter, LV = Likely Voter, null = Unknown
- Output the Data
- Optional: Build the Viz

Author: Kelly Gilbert
Created: 2022-02-02
Requirements:
  - input dataset:
      - PD 2020 Wk 9 Input - Sheet1.csv
  - output dataset (for results check only):
      - PD 2020 Wk 9 Output.csv
"""


from numpy import nan, where
import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in the file, melt the candidates into rows, remove nulls, remove averages
df = pd.read_csv(r'.\inputs\PD 2020 Wk 9 Input - Sheet1.csv', na_values='--')\
       .melt(id_vars=['Poll', 'Date', 'Sample'], var_name='Candidate', value_name='Poll Results')\
       .dropna(subset=['Poll Results'])\
       .query("~Poll.str.contains('Average')", engine='python')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# clean up end date
df['End Date'] = pd.to_datetime(df['Date'].str.extract('.*- (\d+/\d+)', expand=False) + '/2020')
df['End Date'] = where(df['End Date'].dt.month >= 7, 
                       df['End Date'] + pd.DateOffset(years=-1), 
                       df['End Date'])


# form a Rank (modified competition) of the candidates per Poll based on their results
df['Rank'] = df.groupby(['Poll', 'End Date', 'Sample'])['Poll Results'].rank(method='max', ascending=False)\
               .astype(int)
      
        
# difference in poll results between first and second
df['Spread from 1st to 2nd Place'] = \
    df.groupby(['Poll', 'End Date', 'Sample'], as_index=False)['Poll Results']\
      .transform(lambda x: x.max() - x.nlargest(2).min())
               

# rename sample types
sample_map = {'.*RV' : 'Registered Voter', '.*LV' : 'Likely Voter', nan : 'Unknown'}
df['Sample Type'] = df['Sample'].replace(sample_map, regex=True)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Candidate', 'Poll Results', 'Spread from 1st to 2nd Place', 'Rank', 'End Date', 
            'Sample Type', 'Poll']
df.to_csv(r'.\outputs\output-2020-09.csv', index=False, columns=out_cols, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# create chart
#---------------------------------------------------------------------------------------------------

from bokeh.io import output_file
from bokeh.layouts import row
from bokeh.models import CustomJS, Legend, DatetimeTickFormatter, Select, Title
from bokeh.plotting import figure, show

# color constants
color_selected = '#0066cc'
color_deselected = '#bab0ac'

# set the output file path
output_file('dimensions.html')

# subset of registered voters
df_rv = df.loc[df['Sample Type']=='Registered Voter']\
          .sort_values(by=['Candidate', 'End Date', 'Poll'])

# add a figure and format it
p = figure(width=900, height=500, x_axis_type='datetime')
p.add_layout(Title(text='Data from: realclearpolitics.com; Sample Type: Registered Voter', 
                   text_font_size='9pt'), 'above')
p.add_layout(Title(text='2020 Democratic Presidential Nominations', text_font_size="24pt"), 'above')
p.xaxis.formatter=DatetimeTickFormatter(days=["%Y-%m-%d"])
p.y_range.flipped = True
p.add_layout(Legend(), 'right')


# add a line and circles for each candidate option
candidates = sorted(df_rv['Candidate'].unique())

line_dict = {}
circle_dict = {}
for i, c in enumerate(candidates):
    line_dict[c] = p.line(df_rv.loc[df['Candidate']==c]['End Date'], 
                          df_rv.loc[df['Candidate']==c]['Rank'], 
                          legend_label=c, line_width=2,
                          color=color_selected if i==0 else color_deselected)
    
    circle_dict[c] = p.circle(df_rv.loc[df['Candidate']==c]['End Date'], 
                              df_rv.loc[df['Candidate']==c]['Rank'], 
                              legend_label=c, size=7,
                              line_width=0,
                              fill_color=color_selected if i==0 else color_deselected)
    
# create a drop-down menu
menu = Select(options=candidates, value=candidates[0], title='Select an item:')


# link the plot and the button using a callback function

# cb_obj = the model that triggered the callback (e.g. button model, dropdown model)
# args = list of name=object values you want to have accessible inside the callback function
# can't assign cb_obj.value to a model property directly; you have to store it in a variable first

callback = CustomJS(args=dict(p=p, lines=line_dict, circles=circle_dict), code="""
const t = cb_obj.value;

// make the selected item's marks blue and the rest gray
for (let i in lines) {
  if (i == t) {
      lines[i].glyph.line_color = '""" + color_selected + """';
      circles[i].glyph.fill_color = '""" + color_selected + """';
  } else { 
      lines[i].glyph.line_color = '""" + color_deselected + """';
      circles[i].glyph.fill_color = '""" + color_deselected + """';
  }
}
""")

menu.js_on_change('value', callback)    


# display the layout
chart_layout = row(p, menu)
show(chart_layout)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2020 Wk 9 Output.csv']
my_files = ['output-2020-09.csv']
unique_cols = [['Candidate', 'Poll', 'End Date', 'Sample Type']]
col_order_matters = True
round_dec = 8


for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_sol = pd.read_csv('.\\outputs\\' + solution_file, encoding='utf-8')
    df_mine = pd.read_csv('.\\outputs\\' + my_files[i], encoding='utf-8')

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
            print('*** Missing or extra records ***\n')
            print('In solution, not in mine:\n')
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
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]
            if len(unmatched) > 0:
                print(f'*** Values do not match: {c} ***\n')
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                errors += 1
        
        if errors == 0:
            print('Values match')

    print('\n')  
