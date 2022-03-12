# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 10 - The Bechdel Test
https://preppindata.blogspot.com/2022/03/2022-week-10-bechdel-test.html

- Input the data
- Parse out the data in the Download Data field so that we have one field containing the Movie title
  and one field containing information about whether of not the movie passes the Bechdel Test
- Before we deal with the majority of the html codes, I would recommend replacing '&amp;' instances
  with '&' because of this film on the website incorrectly converting the html code 
- Extract the html codes from the Movie titles
    - These will always start with a '&' and end with a ';'
    - The maximum number of html codes in a Movie title is 5
- Replace the html codes with their correct characters
    - Ensure that codes which match up to spaces have a space in their character cell rather than a
      null value
- Parse out the information for whether a film passes or fails the Bechdel test as well as the 
  detailed reasoning behind this
- Rank the Bechdel Test Categorisations from 1 to 5, 1 being the best result, 5 being the worst result
- Where a film has multiple categorisations, keep only the worse ranking, even if this means the 
  movie moves from pass to fail
- Output the data

Author: Kelly Gilbert
Created: 2022-03-11
Requirements:
  - input dataset:
      - PD Bechdel Test.xlsx
  - output dataset (for results check only):
      - Bechdel Test Output.csv
"""


import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\PD Bechdel Test.xlsx') as xl:
    df = pd.read_excel(xl, 'Webscraping')
    df_html = pd.read_excel(xl, 'html')


# rank the Bechdel Test Categorisations from 1 to 5, 1 = best, 5 = worst
ranking_lookup = { 'Fewer than two women in this movie' : 5,
                   'There are two or more women in this movie, but they don\'t talk to ' \
                       'each other' : 4,
                   'There are two or more women in this movie, but they only talk to ' \
                       'each other about a man' : 3,
                   'There are two or more women in this movie and they talk to ' \
                       'each other about something other than a man, although dubious' : 2,
                   'There are two or more women in this movie and they talk to ' \
                       'each other about something other than a man' : 1 }


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# parse out the movie title and categorization
pattern = '.*?/static/(.*?)\.png.*? title=\"\[(.*?)\].*? href.*?>(.*?)<.*'
df[['Pass/Fail', 'Categorisation', 'Movie']] = \
    df['DownloadData'].str.replace('\n', '').str.extract(pattern, expand=True)


# replace html codes 
df_html_m = df_html.melt(id_vars='Char', value_vars=['Numeric', 'Named']).dropna()
df_html_m = pd.concat([df_html_m.loc[df_html_m['variable']=='Numeric'],
                       df_html_m.loc[df_html_m['variable']=='Named'].apply(lambda x: x.str.lower()),
                       df_html_m.loc[df_html_m['variable']=='Named'].apply(lambda x: x.str.title())])\
              .drop_duplicates()
            
char_dict = dict(zip(df_html_m['value'], df_html_m['Char']))

df['Movie'] = df['Movie'].replace(char_dict, regex=True)\
                         .replace(char_dict, regex=True)    # replace twice due to &amp;amp;
            

# clean up pass/fail
df['Pass/Fail'] = df['Pass/Fail'].replace({'nopass' : 'Fail', 'pass' : 'Pass'})


# rank the Bechdel Test Categorisations from 1 to 5
df['Ranking'] = df['Categorisation'].replace(ranking_lookup)


# keep the lowest ranking
df = df.sort_values(by='Ranking', ascending=False)\
       .drop_duplicates(subset=['Movie', 'Year'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.drop(columns='DownloadData').to_csv(r'.\outputs\output-2022-10.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Bechdel Test Output.csv']
my_files = ['output-2022-10.csv']
unique_cols = [['Movie', 'Year']]
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
                print(df_compare[(df_compare['_merge']=='both')
                                 & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])]\
                                [unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                print('\n')
                errors += 1
        
        if errors == 0:
            print('Values match')

    print('\n')  
