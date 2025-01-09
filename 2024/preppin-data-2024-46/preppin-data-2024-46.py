# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 46 - DataFam Europe Special
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
Created: 2024-01-06
Requirements:
  - input dataset:
      - London Visitor Attractions.xlsx
  - output dataset (for results check only):
      - Tube Locations and Attractions.xlsx
"""



import pandas as pd


#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\London Visitor Attractions.xlsx') as xl:

    # stations: deduplicate and rename cols
    df_stations = ( pd.read_excel(xl, 
                                 sheet_name='London Tube Stations',
                                 usecols=['Station', 'Right_Longitude', 'Right_Latitude'])
                     .drop_duplicates() 
                     .rename(columns=lambda c: c.replace('Right_', 'Station '))
                 )
    
    
    # footfall: reshape with years in rows
    df_footfall = ( 
        pd
            .read_excel(xl, sheet_name='Attraction Footfall')
            
            # reshape with years in rows
            .melt(id_vars='Characteristic',
                  var_name='Year', 
                  value_name='Attraction Footfall')
            
            # remove blanks
            .query("`Attraction Footfall` != '-'")
            
            # add calculated fields
            .rename(columns={'Characteristic' : 'Attraction' })
            .assign(**{ 'Attraction Footfall' : 
                            lambda df_x: df_x['Attraction Footfall'].astype(int) * 1000 }
            )           
            .assign(**{ '5 Year Avg Footfall' : 
                            lambda df_x: ( df_x.groupby('Attraction')
                                               ['Attraction Footfall']
                                               .transform('mean')
                                               .astype('int') ),
                        'count' : 
                            lambda df_x: ( df_x.groupby('Attraction')
                                               ['Attraction Footfall']
                                               .transform('count') ) }
            )
                
            # remove partial attractions
            .query("count==5")    
            
            # add rank
            .assign(**{ 'Attraction Rank' : 
                            lambda df_x: ( df_x['5 Year Avg Footfall']
                                              .transform('rank', method='dense', ascending=False)
                                              .astype('int') ) } 
            )
            
            .drop(columns='count')             
    )


    # locations: split lat/lon
    df_locations = ( pd.read_excel(xl, sheet_name='Location Lat  Longs')
                       .assign(
                           **{ 'Attraction Latitude' :
                               lambda df_x: df_x['Lat, Longs'].str.extract(r'(.*)\, .*').astype(float),
                               'Attraction Longitude' : 
                               lambda df_x: df_x['Lat, Longs'].str.extract(r'.*\, (.*)').astype(float) }
                       )
                       .drop(columns='Lat, Longs')
                    )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

with pd.ExcelWriter(r'.\outputs\output-2024-46.xlsx') as writer:
    df_stations.to_excel(writer, sheet_name='Tube Locations', index=False)
    df_footfall.to_excel(writer, sheet_name='Attraction Footfall', index=False)
    df_locations.to_excel(writer, sheet_name='Attraction Locations', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Tube Locations and Attractions.xlsx']
my_files = ['output-2024-46.xlsx']
col_order_matters = False

pd.set_option('display.width', 300)
pd.set_option('display.max_columns', 10)
pd.set_option('display.max_colwidth', 50)


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

