# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 46 - DataFam Europe Special (polars)
https://preppindata.blogspot.com/2024/11/2024-week-46-datafam-europe-special.html

- Input the data
- For the London Tube Stations table:
  - There are a lot of unnecessary fi elds, only keep information about the stationname and location
  - Clean up the fi eld names
  - There are a lot of duplicate rows. Make sure each row is unique 
- For the Attraction Footfall table:
  - Filter out attractions with missing data
  - Reshape the data so there is a row for each year, for each attraction
  - The footfall values need to be multiplied by 1000 to give their true values
  - Calculate the average footfall for each attraction, whilst keeping all the detail ofindividual years. Call the new fi eld 5 Year Avg Footfall
  - Rank the attractions based on this 5 Year Avg Footfall
- For the Location Lat Longs table
  - The information about the latitude and longitude is contained in a single fi eld, splitthese values into 2 separate fi elds
- Output the data as an Excel File, having each table as a separate sheet

Author: Kelly Gilbert
Created: 2024-01-08
Requirements:
  - input dataset:
      - London Visitor Attractions.xlsx
  - output dataset (for results check only):
      - Tube Locations and Attractions.xlsx
"""


import pandas as pd    # for results check only
import polars as pl
from xlsxwriter import Workbook


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

input_path = r'.\inputs\London Visitor Attractions.xlsx'


# stations: deduplicate and rename cols
df_stations = ( 
    pl
        .read_excel(input_path, 
                   sheet_name='London Tube Stations',
                   columns=['Station', 'Right_Longitude', 'Right_Latitude'])
        .unique()
        .select(
            pl.all().name.map(lambda c: c.replace('Right_', 'Station '))
        )
)

    
# footfall: reshape with years in rows; add 5-yr average and rank
df_footfall = ( 
    pl
        .read_excel(input_path, sheet_name='Attraction Footfall')
        
        # reshape with years in rows
        .unpivot(
            index='Characteristic',
            variable_name='Year', 
            value_name='Attraction Footfall'
        )
        
        # remove blanks
        .filter(pl.col('Attraction Footfall') != '-')
        
        # add calculated fields
        .rename({'Characteristic' : 'Attraction' }) 
        .with_columns(
            (pl.col('Attraction Footfall').cast(pl.Int32) * pl.lit(1000))
               .alias('Attraction Footfall')
        )
        .with_columns(
            pl.col('Attraction Footfall').mean().over('Attraction')
              .cast(pl.Int32)
              .alias('5 Year Avg Footfall'),
            pl.col('Attraction Footfall').count().over('Attraction')
              .cast(pl.Int16)
              .alias('count')
        )
        .filter(pl.col('count') == 5)
        .drop(pl.col('count'))
        
        # add rank
        .with_columns(
            pl.col('5 Year Avg Footfall').rank(method='dense', descending=True)
              .cast(pl.Int16)
              .alias('Attraction Rank')
        )       
) 


# locations: split lat/lon into columns
df_locations = ( 
    pl
        .read_excel(input_path, sheet_name='Location Lat  Longs')
        .with_columns( 
            pl.col('Lat, Longs').str.split_exact(', ', n=2)
              .struct.rename_fields(['Attraction Latitude', 'Attraction Longitude'])
        )
        .unnest('Lat, Longs') 
)
        

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

with Workbook(r'.\outputs\output-2024-46.xlsx') as wb:
    df_stations.write_excel(wb, worksheet='Tube Locations')
    df_footfall.write_excel(wb, worksheet='Attraction Footfall')
    df_locations.write_excel(wb, worksheet='Attraction Locations')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Tube Locations and Attractions.xlsx']
my_files = ['output-2024-46.xlsx']
col_order_matters = False


for i, solution_file in enumerate(solution_files):
    xl_solution = pd.ExcelFile('.\\outputs\\' + solution_file)
    xl_mine = pd.ExcelFile('.\\outputs\\' + my_files[i])

    for s in xl_solution.sheet_names:

        print('---------- Checking \'' + solution_file + '\', sheet \'' + s + '\' ----------\n')

        # read in the files
        df_solution = pd.read_excel(xl_solution, s)
        df_mine = pd.read_excel(xl_mine, s)

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

