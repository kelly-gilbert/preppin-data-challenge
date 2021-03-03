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
with ExcelFile(r'.\\inputs\\Shopping List and Ingredients.xlsx') as xl:
    dfItems = read_excel(xl, 'Shopping List')
    dfKeywordsIn = read_excel(xl, 'Keywords')

# parse the keywords and numbers, stack the names and numbers, add E to the numbers
keywordList = ['E' + k if k.isnumeric() else k 
               for k in dfKeywordsIn.stack().str.split(', ').explode().reset_index(drop=True)]

    
    
#--------------------------------------------------------------------------------
# method 1: list comprehension
#    The challenge specifically said to append the keywords (i.e. a cartesian
#    product, method #2 below). In practice, I would accomplish this using a
#    list comprehension.
#--------------------------------------------------------------------------------

# parse the keywords and numbers, stack the names and numbers, add E to the numbers
dfKeywords = ['E' + k if k.isnumeric() else k 
              for k in dfKeywordsIn.stack().str.split(', ').explode().reset_index(drop=True)]
    
dfItems['Contains'] = [', '.join([k.lower() for k in dfKeywords if k in i]) 
                       for i in dfItems['Ingredients/Allergens']]

    
#--------------------------------------------------------------------------------
# method 2: cartesian product (as specified in the challenge)
#--------------------------------------------------------------------------------
    
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

dfItems = dfAll.groupby(['Product','Description'])['Contains'].agg(Contains=list).reset_index()
dfItems['Contains'] = [', '.join([i for i in c if i != '']) for c in dfItems['Contains']]


#--------------------------------------------------------------------------------
# output the files
#--------------------------------------------------------------------------------

dfItems[dfItems['Contains'] == ''].to_csv('.\\\\outputs\\\\output-2021-07-vegan.csv', 
                                       columns=['Product', 'Description'], index=False)
dfItems[dfItems['Contains'] != ''].to_csv('.\\\\outputs\\\\output-2021-07-non-vegan.csv', 
                                       columns=['Product', 'Description', 'Contains'], index=False)


#--------------------------------------------------------------------------------
# check results
#--------------------------------------------------------------------------------

solutionFiles = ['Vegan List.csv', 'Non Vegan List.csv']
myFiles = ['output-2021-07-vegan.csv', 'output-2021-07-non-vegan.csv']
col_order_matters = False

for i in range(len(solutionFiles)):
    print('---------- Checking \'' + solutionFiles[i] + '\' ----------\n')
    
    # read in the files
    dfSolution = read_csv('.\\outputs\\' + solutionFiles[i])
    dfMine = read_csv('.\\outputs\\' + myFiles[i])
    
    # are the fields the same and in the same order?
    solutionCols = list(dfSolution.columns)
    myCols = list(dfMine.columns)
    if col_order_matters == False:
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
    if col_match == True:
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