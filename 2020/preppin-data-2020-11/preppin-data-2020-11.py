# -*- coding: utf-8 -*-
"""
Preppin' Data 2020: Week 11
https://preppindata.blogspot.com/2020/03/2020-week-11.html

- Input the data.
- For each order, figure out how many boxes of each size will be required.
- Arrange this information so there is a single row per order with different fields for each box size.
- Output the above.

- For each box, figure out how many bars of soap will be in that box.
- Assign each box in each order a unique ID, starting from 1 each in each order.
- The box ID should be ascending from the box with the most soap to the box with the least.
- Output the above as well.

Author: Kelly Gilbert
Created: 2022-01-21
Requirements:
  - input dataset:
      - PD 2020 Week 11 Input.xlsx
  - output dataset (for results check only):
      - PD 2020 Wk 11 Output - Soaps per Box.csv
"""

import numpy as np
import pandas as pd


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def get_box_sizes(order_sizes, size_list):
    """
    Returns columns containing the number of boxes needed for each box size
    
    order_sizes: a series containing the order sizes
    size_list: a list of box sizes
    
    returns: a dataframe with columns for each box size
    """    

    df = pd.DataFrame({'Order Size' : order_sizes})\
           .assign(Remainder=lambda df_x: df_x['Order Size'])
    size_list.sort(reverse=True)
    
    for i, s in enumerate(size_list):
        if i < len(size_list) - 1:
            df[f'Boxes of {s}'] = df['Remainder'] // s
            df['Remainder'] = df['Remainder'] % s
        else:
            df[f'Boxes of {s}'] = (np.ceil(df['Remainder'] / s)).astype(int)
            
    return df.drop(columns=['Order Size', 'Remainder'])


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\PD 2020 Week 11 Input.xlsx') as xl:
    df_orders = pd.read_excel(xl, sheet_name='Orders') 
    df_sizes = pd.read_excel(xl, sheet_name='Box Sizes')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# for each order, figure out how many boxes of each size will be required.
df_boxes = pd.concat([df_orders, 
                      get_box_sizes(df_orders['Order Size'], list(df_sizes['Box Size']))],
                      axis=1)

# create one row per box
df_soaps = df_boxes.melt(id_vars=['Order Number', 'Order Size'], var_name='Box_Size', 
                         value_name='Size Count')\
                   .assign(Box_Size=lambda df_x: df_x['Box_Size'].str.replace('Boxes of ', '').astype(int),
                           Box_Number=lambda df_x: [range(1, c+1) for c in df_x['Size Count']])\
                   .explode('Box_Number')\
                   .dropna(subset=['Box_Number'])\
                   .rename(columns=lambda c: c.replace('_', ' '))
                   
df_soaps['Box Number'] = df_soaps.groupby('Order Number')['Box Number'].transform('cumcount') + 1

df_soaps['Last Box Per Box Size'] = df_soaps.groupby(['Order Number', 'Box Size'])['Box Number'].transform('max')

df_soaps['Soaps in Box'] = np.where((df_soaps['Box Size']==df_sizes['Box Size'].min()) 
                                     & (df_soaps['Box Number']==df_soaps['Last Box Per Box Size']),
                                    df_soaps['Order Size'] % df_sizes['Box Size'].min(),
                                    df_soaps['Box Size'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_boxes.to_csv(r'.\outputs\output-2020-11-boxes-per-order.csv', index=False)
df_soaps.drop(columns=['Size Count'])\
        .to_csv(r'.\outputs\output-2020-11-soaps-per-box.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2020 Wk 11 Output - Boxes per Order.csv', 
                  'PD 2020 Wk 11 Output - Soaps per Box.csv']
my_files = ['output-2020-11-boxes-per-order.csv', 
            'output-2020-11-soaps-per-box.csv']
unique_cols = [['Order Number'], ['Order Number', 'Box Size', 'Box Number']]
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


df_sol[df_sol['Order Number']==5][['Box Size', 'Box Number']]
df_mine[df_sol['Order Number']==5][['Box Size', 'Box Number']]
df_soaps[df_soaps['Order Number']==5]
