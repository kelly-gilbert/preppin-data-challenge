# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 9 - Working with Strings
https://preppindata.blogspot.com/2021/03/2021-week-9-working-with-strings.html

- Input the Customer Information file, split the values and reshape the data so there is a separate
  ID on each row.
- Each ID field contains the following information we need to extract:
    - The first 6 digits present in each ID is the customers phone number
    - The first 2 digits after the ‘,’ is the last 2 digits of the area code
    - The letter following this is the first letter of the name of the area that they are calling from
    - The digits after this letter resemble the quantity of products ordered
    - The letters after the ‘-‘ are the product ID codes
- Rename these fields appropriately, and remove any unwanted columns – leaving only these 5 columns
  in the workflow.
- Input the Area Code Lookup Table – find a way to join it to the Customer information file
- We don’t actually sell products in Clevedon, Fakenham, or Stornoway. Exclude these from our dataset
- In some cases, the ID field does not provide accurate enough conditions to know where the customer
  is from. Exclude any phone numbers where the join has produced duplicated records.
- Remove any unwanted fields created from the join.
- Join this dataset to our product lookup table.
- For each area, and product, find the total sales values, rounded to zero decimal places
- Rank how well each product sold in each area.
- For each area, work out the percent of total that each different product contributes to the overall
  revenue of that Area, rounded to 2 decimal places.
- Output the data

Author: Kelly Gilbert
Created: 2021-03-15
Requirements:
  - Pandas 0.25.0 or higher (for explode)
  - input datasets:
      - Area Code Lookup.xlsx
      - Customer Information.xlsx
      - Product Lookup.xlsx
  - output dataset (for results check):
      - Preppin Data 2020W9 Output.csv

"""

from pandas import DataFrame, read_excel
from numpy import floor, vectorize

# used for answer check only
from pandas import read_csv


def round_half_up(n, decimals=0):
    """ 
    use round half up method vs. Python default rounding
    """
    multiplier = 10 ** decimals
    # Replace math.floor with np.floor
    return floor(n*multiplier + 0.5) / multiplier

round_half_up_v = vectorize(round_half_up)


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

customer_info = read_excel('.\\inputs\\Customer Information.xlsx')['IDs'].str.split(' ').explode()
areas = read_excel('.\\inputs\\Area Code Lookup.xlsx')
products = read_excel('.\\inputs\\Product Lookup.xlsx')

# parse the customer info
extract_regex = r'\D*?(?P<phone>\d{6}).*?\,(?P<join>\d{2}\w)(?P<ordered>\d+)-(?P<product_id>.+)'
customers = DataFrame(customer_info)['IDs'].str.extract(extract_regex)
customers['ordered'] = customers['ordered'].astype(int)

# clean the price
products['Price'] = products['Price'].str.strip('£').astype(float)

# remove areas with duplicate first letter/last 2 digits
areas['join'] = areas['Code'].astype(str).str.slice(-2) + areas['Area'].str.slice(stop=1)
areas['count'] = areas.groupby('join')['join'].transform('count')

# remove unnecessary areas
remove_areas = ['Clevedon', 'Fakenham', 'Stornoway']
areas = areas[(areas['count'] == 1) & (~areas['Area'].isin(remove_areas))]

# join area and product info to customers
customers = customers.merge(areas, on='join', how='inner')


#---------------------------------------------------------------------------------------------------
# calculate sales and ranks
#---------------------------------------------------------------------------------------------------

# group by area/item
area_item = customers.groupby(['Area', 'product_id'])[['ordered']].sum().reset_index()

# calculate the revenue per item and % of area
area_item = area_item.merge(products, left_on='product_id', right_on='Product ID', how='inner')
area_item['Revenue'] = round_half_up_v(area_item['ordered'] * area_item['Price'], 0).astype(int)

area_item['% of Total - Product'] = \
    round_half_up_v((area_item['Revenue'] / area_item.groupby('Area')['Revenue'].transform('sum')) * 100, 2)

# add the rank
area_item['Rank'] = area_item.groupby('Area').rank(ascending=False)[['Revenue']].astype(int)


#---------------------------------------------------------------------------------------------------
# output the data
#---------------------------------------------------------------------------------------------------

area_item.to_csv('.\\outputs\\output-2021-09.csv', index=False,
                 columns=['Rank', 'Area', 'Product Name', 'Revenue', '% of Total - Product'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solutionFiles = ['Preppin Data 2020W9 Output.csv']
myFiles = ['output-2021-09.csv']
col_order_matters = False


for i in range(len(solutionFiles)):
    print('\n---------- Checking \'' + solutionFiles[i] + '\' ----------\n')

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
