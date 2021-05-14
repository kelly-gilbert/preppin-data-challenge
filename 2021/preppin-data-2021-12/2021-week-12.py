# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 12 - Maldives Tourism
https://preppindata.blogspot.com/2021/03/2021-week-12-maldives-tourism.html

- Input the data
- Pivot all of the month fields into a single column
- Rename the fields and ensure that each field has the correct data type
- Filter out the nulls
- Filter our dataset so our Values are referring to Number of Tourists
- Our goal now is to remove all totals and subtotals from our dataset so that only the lowest level
  of granularity remains. Currently we have Total > Continents > Countries, but we don't have data
  for all countries in a continent, so it's not as simple as just filtering out the totals and
  subtotals. Plus in our Continents level of detail, we also have The Middle East and UN passport
  holders as categories. If you feel confident in your prep skills, this (plus the output) should be
  enough information to go on, but otherwise read on for a breakdown of the steps we need to take:
    - Filter out Total tourist arrivals
    - Split our workflow into 2 streams: Continents and Countries
      Hint: the hierarchy field will be useful here
    - Split out the Continent and Country names from the relevant fields
    - Aggregate our Country stream to the Continent level
    - Join the two streams together and work out how many tourists arrivals there are that we don't
      know the country of
    - Add in a Country field with the value "Unknown"
    - Union this back to here we had our Country breakdown
- Output the data

Author: Kelly Gilbert
Created: 2021-03-24
Requirements:
  - seaborn version 0.11.0 (for axes_dict and crest palette)
  - input dataset:
      - Tourism Input.csv
  - output dataset (for results check):
      - Preppin Data 2020W9 Output.csv

"""


from numpy import nan, where
from pandas import concat, melt, merge, read_csv, to_datetime

# for the charts
import seaborn as sns
from matplotlib import pyplot as plt


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in the data, then stack it
key_cols = ['Series-Measure', 'Hierarchy-Breakdown', 'Unit-Detail']

df = read_csv(r'.\inputs\Tourism Input.csv', na_values=['na'])\
         .drop(columns=['id'])\
         .melt(id_vars=key_cols)\
         .rename(columns={'variable':'Month'})

df['Month'] = to_datetime(df['Month'], format='%b-%y')


#---------------------------------------------------------------------------------------------------
# prep the data
#---------------------------------------------------------------------------------------------------

# filter for tourist arrival counts and remove null values
df = df.loc[(df['Series-Measure'].str.contains('Tourist arrivals')) & (df['value'].notna())]
df['value'] = df['value'].astype(int)

# extract the country and continent
df['Country'] = where(df['Hierarchy-Breakdown'].str.match('.*Tourist arrivals / .*'),
                      df['Series-Measure'].str.replace('Tourist arrivals from (the )?', ''), nan)

df['Breakdown'] = where(df['Hierarchy-Breakdown'].str.match('.*Tourist arrivals / .*'),
                        df['Hierarchy-Breakdown'].str.replace('.*Tourist arrivals / ', ''),
                        df['Series-Measure'].str.\
                            replace('Tourist arrivals from |Tourist arrivals - ', ''))

# sum country values by continent
cont_dtl = df[df['Country'].notna()].groupby(['Breakdown', 'Month'])['value'].sum().reset_index()

# join the continent totals to the sums to find the difference
cont_tot = df.loc[df['Country'].isna()]
cont_tot = cont_tot.merge(cont_dtl, on=['Breakdown', 'Month'], suffixes=['', '_CountryTotal'],
                          how='left')
cont_tot['value'] = cont_tot['value'] - cont_tot['value_CountryTotal'].fillna(0)

# remove the continent totals and union the new Unknown-country rows to the main dataframe
cont_tot['Country'] = 'Unknown'
cont_tot.drop(columns=['value_CountryTotal'], inplace=True)
df = concat([df[df['Country'].notna()], cont_tot])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.rename(columns={'value':'Number of Tourists'}, inplace=True)
df.to_csv('.\\outputs\\output-2021-12.csv', index=False, date_format='%d/%m/%Y',
          columns=['Breakdown', 'Month', 'Number of Tourists', 'Country'])


#---------------------------------------------------------------------------------------------------
# generate the charts
#---------------------------------------------------------------------------------------------------

charts_per_row = 3
sns.set_style("white")
sort=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

# summarize the data by region and year/month
df_region = df.groupby(['Breakdown', 'Month'])['Number of Tourists'].sum().reset_index()
df_region['Year'] = df_region['Month'].dt.year.astype(int)
df_region['Month Name'] = df_region['Month'].dt.strftime('%b')

# draw a grid of charts, one for each region, where x=month, y=# arrivals, and line per year
g = sns.relplot(kind='line', data=df_region, x='Month Name', y='Number of Tourists', units='Year', 
                hue='Year', col='Breakdown', palette='GnBu', linewidth=1, estimator=None, 
                col_wrap=charts_per_row, height=2.5, aspect=1.5, sort=sort, legend=True,
                facet_kws={'sharex':True, 'sharey':False, 'legend_out':True}).add_legend()

# place the legend
g._legend.set_bbox_to_anchor([1.1, 0])

# add spacing to the grid
g.fig.tight_layout(h_pad=4, w_pad=4)  

# add an orange line for the current year
for Breakdown, ax in g.axes_dict.items():
    # overlay the last year in orange
    sns.lineplot(data=df_region[(df_region['Year']==df_region['Year'].max()) 
                                & (df_region['Breakdown']==Breakdown)],
                 x='Month Name', y='Number of Tourists',  color='orange',
                 linewidth=3, ci=None, sort=sort, ax=ax, legend=None)
    ax.set_title(f"{Breakdown}")
    ax.set(xlabel=None, ylabel=None)
    
# add the main title
g.fig.suptitle('Maldives Tourist Arrivals by Region and Year', x=0.58, y=1.1, fontsize='xx-large')
g.fig.text(s='Most recent year (' + str(df_region['Year'].max()) + ') is highlighted', 
          x=0.46, y=1.04, size='12')
plt.show()


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solutionFiles = ['Tourism Output.csv']
myFiles = ['output-2021-12.csv']
col_order_matters = False

for i in range(len(solutionFiles)):
    print('---------- Checking \'' + solutionFiles[i] + '\' ----------\n')

    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solutionFiles[i])
    dfMine = read_csv('.\\outputs\\' + myFiles[i])

    # are the fields the same and in the same order?
    solutionCols = list(dfSolution.columns)
    myCols = list(dfMine.columns)
    if not col_order_matters:
         solutionCols.sort()
         myCols.sort()

    col_match = False
    if solutionCols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(dfSolution.columns)))
        print('    Columns in mine    : ' + str(list(dfMine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        dfSolution['join'] = 1
        dfMine['join'] = 1
        dfCompare = dfSolution.merge(dfMine, how='outer', on=list(dfSolution.columns)[:-1])
        dfCompare.rename(columns={'join_x':'in_solution', 'join_y':'in_mine'}, inplace=True)

        if dfCompare['in_solution'].count() != len(dfCompare):
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')

    print('\n')
