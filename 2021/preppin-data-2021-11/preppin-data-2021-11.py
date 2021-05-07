# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 7 - Cocktail Profit Margins
https://preppindata.blogspot.com/2021/03/2021-week-11-cocktail-profit-margins.html
 
- Input the dataset 
- Split out the recipes into the different ingredients and their measurements
- Calculate the price in pounds, for the required measurement of each ingredient
- Join the ingredient costs to their relative cocktails
- Find the total cost of each cocktail 
- Include a calculated field for the profit margin i.e. the difference between each cocktail's price
  and its overall cost 
- Round all numeric fields to 2 decimal places 
- Output the data

Author: Kelly Gilbert
Created: 2021-03-21
Requirements: 
  - pandas version 0.25.0 or higher (for explode)
  - input dataset (Shopping List and Ingredients.xlsx)
  - output dataset (for results check):
    - Vegan List.csv
    - Non Vegan List.csv
  
"""


from pandas import ExcelFile, read_excel

# used for answer check only
from pandas import read_csv


# --------------------------------------------------------------------------------------------------
# input the data
# --------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Cocktails Dataset.xlsx') as xl:
    cocktails = read_excel(xl, 'Cocktails', index_col='Cocktail')
    src = read_excel(xl, 'Sourcing')
    conv_dict = read_excel(xl, 'Conversion Rates', index_col = 'Currency', squeeze=True).to_dict()


# --------------------------------------------------------------------------------------------------
# prep / calculations
# --------------------------------------------------------------------------------------------------

# parse the recipes
regex_str = r'(?P<Ingredient>.+)\:(?P<ml>\d+)ml'
recipes = cocktails['Recipe (ml)'].str.split('; ').explode().str.extract(regex_str, expand=True)

# convert ingredient prices to pounds
src['price_pounds'] = [p / conv_dict[c] for c,p in zip(src['Currency'], src['Price'])] 

# calculate the cocktail cost in pounds
cols = ['Ingredient','ml per Bottle', 'price_pounds']
recipes = recipes.reset_index().merge(src[cols], on='Ingredient', how='left')

recipes['Cost'] = recipes.apply(lambda r: round(float(r['ml']) * r['price_pounds'] 
                                                      / r['ml per Bottle'], 2), axis=1) 

# total cost by cocktail
costs = recipes.groupby('Cocktail')[['Cost']].sum()

# calculate profit 
final = cocktails.merge(costs, on='Cocktail', how='left').rename(columns = {'Price (£)':'Price'})
final['Margin'] = round(final['Price'] - final['Cost'], 2)


# --------------------------------------------------------------------------------------------------
# output the data
# --------------------------------------------------------------------------------------------------

final.reset_index().to_csv(r'.\outputs\output-2021-11.csv', index=False, 
                           columns=['Margin','Cost','Cocktail','Price'])


# ---------------------------------------------------------------------------------------------------
# check results
# ---------------------------------------------------------------------------------------------------

solutionFiles = ['PD 2021 Wk 11 Output.csv']
myFiles = ['output-2021-11.csv']
col_order_matters = False


for i in range(len(solutionFiles)):
    print('\n---------- Checking \'' + myFiles[i] + '\' ----------\n')

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

        if len(dfCompare[dfCompare['in_solution'].isna() | dfCompare['in_mine'].isna()]) > 0:
            print('*** Values do not match ***')
            print(dfCompare[dfCompare['in_solution'] != dfCompare['in_mine']])
        else:
            print('Values match')

    print('\n')
