# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 29 - PD x WOW - Tokyo 2020 Calendar
https://preppindata.blogspot.com/2021/07/2021-week-29-pd-x-wow-tokyo-2020.html

- Input the Data 
- Create a correctly formatted DateTime field
- Parse the event list so each event is on a separate row
- Group similar sports into a Sport Type field
- Combine the Venue table
- Calculate whether the event is a 'Victory Ceremony' or 'Gold Medal' event. 
  (Note, this might not pick up all of the medal events.)
- Output the Data

Author: Kelly Gilbert
Created: 2021-08-11
Requirements:
  - input dataset:
      - Olympic Events.xlsx
  - output dataset (for results check only):
      - Olympic Events Schedule.xlsx
"""


from pandas import ExcelFile, ExcelWriter, read_excel, to_datetime
from re import IGNORECASE

sports_map = { '3X3 Basketball' : '3x3 Basketball',
               'Artistic Gymnastic' : 'Artistic Gymnastics',
               'Baseball' : 'Baseball/Softball',
               'Beach Volleybal' : 'Beach Volleyball', 
               'Beach Volley' : 'Beach Volleyball',
               'Cycling Bmx Racing' : 'Cycling BMX Racing',
               'Cycling Bmx Freestyle' : 'Cycling BMX Freestyle',
               'Softball' : 'Baseball/Softball',
               'Softball/Baseball' : 'Baseball/Softball'}

group_map = { '3X3 Basketball' : 'Basketball',
              'Artistic Gymnastic' : 'Gymnastics',
              'Artistic Gymnastics' : 'Gymnastics',
              'Artistic Swimming' : 'Swimming',
              'Baseball/Softball' : 'Baseball',
              'Beach Volleyball' : 'Volleyball',
              'Canoe Slalom' : 'Canoeing',
              'Canoe Sprint' : 'Canoeing',
              'Closing Ceremony' : 'Ceremony',
              'Cycling Bmx Freestyle' : 'Cycling',
              'Cycling Bmx Racing' : 'Cycling',
              'Cycling Mountain Bike' : 'Cycling',
              'Cycling Road' : 'Cycling',
              'Cycling Track' : 'Cycling',
              'Judo' : 'Martial Arts',
              'Karate' : 'Martial Arts',
              'Marathon Swimming' : 'Swimming',
              'Opening Ceremony' : 'Ceremony',
              'Table Tennis' : 'Tennis',
              'Taekwondo' : 'Martial Arts',
              'Trampoline Gymnastics' : 'Gymnastics'
            }


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\inputs\Olympic Events.xlsx') as xl:
    events = read_excel(xl, 'Olympics Events')
    venues = read_excel(xl, 'Venues')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create a correctly formatted DateTime field
events['UK Date Time'] = to_datetime(events['Date'].str.replace('(?<=\d)[a-z]+', '') + ' ' 
                                         + events['Time'].str.replace('xx', '0:00'), 
                                     format='%d_%B_%Y %H:%M')
events['Date'] = events['UK Date Time'].dt.date


# clean the sport name and group similar sports into a Sport Type field
events['Sport'] = events['Sport'].str.replace('\.', '').str.title().replace(sports_map)
events['Sport Group'] = events['Sport'].str.title().replace(group_map)


# parse the event list so each event is on a separate row
events['Events Split'] = [[e.strip() for e in es] for es in events['Events'].str.split(',')]
events = events.explode('Events Split')


# calculate victory/medal events
events['Medal Ceremony?'] = events['Events Split'].str.contains('Gold Medal|Victory Ceremony', 
                                                                flags=IGNORECASE)


# combine the Venue table
events['Venue_lower'] = events['Venue'].str.lower()
venues['Venue_lower'] = venues['Venue'].str.lower()
venues[['Latitude', 'Longitude']] = venues['Location'].str.extract('(.*), (.*)')
final = events.merge(venues[['Venue_lower', 'Latitude', 'Longitude']].drop_duplicates(), 
                     on='Venue_lower')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Latitude', 'Longitude', 'Medal Ceremony?', 'Sport Group', 'Events Split', 
            'UK Date Time', 'Date', 'Sport', 'Venue']

with ExcelWriter(r'.\outputs\output-2021-29.xlsx') as xl:
    final[out_cols].to_excel(xl, index=False, sheet_name='Event Schedule')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Olympic Event Schedule.xlsx']
my_files = ['output-2021-29.xlsx']
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
    
            # add the original indices
            df_solution.reset_index(inplace=True)
            df_mine.reset_index(inplace=True)
                        
            
            # WEEK 29 ONLY: convert all sport names to title case
            df_solution['Sport'] = df_solution['Sport'].str.title().str.replace('3X3', '3x3')
            df_solution['Sport Group'] = df_solution['Sport Group'].str.title()
            
           
            # join the dataframes on all columns except the indices
            on_cols = [c for c in df_solution.columns if c not in ['index']]
            df_solution_compare = df_solution.merge(df_mine, how='outer',
                                                    on=on_cols, suffixes=['_solution', '_mine'], 
                                                    indicator=True)
    
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
