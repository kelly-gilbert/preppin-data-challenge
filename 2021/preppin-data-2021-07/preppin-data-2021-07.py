# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 7 - Vegan Shopping List
https://preppindata.blogspot.com/2021/02/2021-week-7-vegan-shopping-list.html
 
- Input the data
- Prepare the keyword data
    - Add an 'E' in front of every E number.
    - Stack Animal Ingredients and E Numbers on top of each other.
    - Get every ingredient and E number onto separate rows.
- Append the keywords onto the product list.
- Check whether each product contains any non-vegan ingredients.
- Prepare a final shopping list of vegan products.
    - Aggregate the products into vegan and non-vegan.
    - Filter out the non-vegan products.
- Prepare a list explaining why the other products aren't vegan.
    - Keep only non-vegan products.
    - Duplicate the keyword field.
    - Rows to columns pivot the keywords using the duplicate as a header.
    - Write a calculation to concatenate all the keywords into a single comma-separated list for each product, e.g. "whey, milk, egg".
- Output the data

Author: Kelly Gilbert
Created: 2021-02-17
Requirements: 
  - pandas v 0.25.0 or higher (for explode())
  - input dataset (Shopping List and Ingredients.xlsx)
  - output dataset (for results check):
    - Vegan List.csv
    - Non Vegan List.csv
  
"""

from pandas import DataFrame, ExcelFile, read_excel

# used for answer check only
from pandas import read_csv


# import the data
with ExcelFile(r'.\inputs\Shopping List and Ingredients.xlsx') as xl:
    dfItems = read_excel(xl, 'Shopping List')
    dfKeywordsIn = read_excel(xl, 'Keywords')
   
    
# prepare the keyword data:
# parse the keywords and numbers, stack the names and numbers, add E to the numbers
dfKeywords = DataFrame(dfKeywordsIn.stack().str.split(', ').explode().rename('keyword'))
dfKeywords.reset_index(drop=True, inplace=True)
dfKeywords['keyword'] = ['E' + k if k.isnumeric() else k for k in dfKeywords['keyword']]


# append the keywords onto the product list (i.e. create a cartesian product)
dfKeywords['join'] = 1
dfItems['join'] = 1
dfAll = dfItems.merge(dfKeywords, on='join')


# check for keyword in ingredient list
dfAll['Contains'] = [k.lower() if k.lower() in i.lower() else ''
                     for i,k in zip(dfAll['Ingredients/Allergens'], dfAll['keyword'])]


# concatenate the keywords into a list
dfAll.drop_duplicates(subset=['Product', 'Description', 'Contains'])

dfOut = dfAll.groupby(['Product','Description'])['Contains'].agg(Contains=list).reset_index()
dfOut['Contains'] = [', '.join([i for i in c if i != '']) for c in dfOut['Contains']]


# output the files
dfOut[dfOut['Contains'] == ''].to_csv('.\\outputs\\output-2021-07-vegan.csv', 
                                       columns=['Product', 'Description'], index=False)
dfOut[dfOut['Contains'] != ''].to_csv('.\\outputs\\output-2021-07-non-vegan.csv', index=False)


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solution_files = ['Vegan List.csv', 'Non Vegan List.csv']
my_files = ['output-2021-07-vegan.csv', 'output-2021-07-non-vegan.csv']
col_order_matters = False

i=1
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
    