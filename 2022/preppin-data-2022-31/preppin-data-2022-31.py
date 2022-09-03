# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 31 - C&BSCo Preppin' Parameters
https://preppindata.blogspot.com/2022/08/2022-week-31-c-preppin-parameters.html

- Input the data
- Split the Product Name field into Product Type and Size
- Only keep the Liquid products
- Total up the sales for each Product Size and Scent for each Store
- Rank each of the Product Size and Scent combinations for each Store
- Only leave the top 10 based on total sales value calculated above
- Round the Sales Values to the nearest 10 value (ie 1913 becomes 1910)
- Create a parameter to select the store
- Ensure the output only contains the chosen store
- Output the data and include the Store Name in the file name

Author: Kelly Gilbert
Created: 2022-08-30
Requirements:
  - input dataset:
      - Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv
  - output dataset (for results check only):
      - PD 2022 Wk 31 Top 10 Products for [store name].csv (six files)
"""


import pandas as pd
# from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# function
#---------------------------------------------------------------------------------------------------

def output_data(df, store_name):
    """
    Prep data and output the file for the selected store.
    """
    
    # keep liquid and selected store
    df_store = df.loc[(df['Store Name']==store_name) & (df['Product Name'].str.contains('Liquid')),
                      df.columns]
    
    # split the Product Name field into Product Type and Size
    df_store[['Product Type', 'Size']] = df_store['Product Name'].str.extract('(.*) - (.*)')
    
    # rank based on sales and keep the top 10
    df_store['Rank of Product & Scent by Store'] = \
        df_store['Sale Value'].rank(method='first', ascending=False)
    df_out = df_store.loc[df_store['Rank of Product & Scent by Store'] <= 10, df_store.columns]
    
    # round the Sales Values to the nearest 10 value (ie 1913 becomes 1910)
    df_out['Sale Value'] = df_out['Sale Value'].round(-1)

    # output the file    
    df_out.to_csv(f'.\\outputs\\output-2022-31-{store_name}.csv', index=False,
                  columns=['Store Name', 'Rank of Product & Scent by Store', 'Scent Name', 
                           'Size', 'Sale Value'])
    
    print(f'\n*** SUCCESS: the file for {store_name} has been created.\n')


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input the file and sum sales by product, scent, and store
df = ( pd.read_csv(r".\inputs\Preppin' Summer 2022 - PD 2022 Wk 27 Input.csv")
         .groupby(['Product Name', 'Scent Name', 'Store Name'], as_index=False)['Sale Value'].sum() 
     )


#---------------------------------------------------------------------------------------------------
# get user input and output the file
#---------------------------------------------------------------------------------------------------

store_list = sorted(df['Store Name'].unique())
store_list_str = '\n  '.join([f'{i+1} - {n}' for i,n in enumerate(store_list)])

while True:
    input_num = input('\nStore list:\n  ' + store_list_str + '\n\n' 
                      + 'Please enter a number (or press Enter to quit): ')
    
    if input_num.isnumeric() and int(input_num) in range(1, len(store_list)+2):
        output_data(df, store_list[int(input_num)-1])
        
    elif input_num == '':
        break
    
    else:    
        print(f'\n*** ERROR: {input_num} is not a valid number.\n')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# solution_files = [f'.\\outputs\\PD 2022 Wk 31 Top 10 Products for {store_list[int(input_num)-1]}.csv']
# my_files = [f'.\\outputs\\output-2022-31-{store_list[int(input_num)-1]}.csv']
# unique_cols = [['Size', 'Scent Name', 'Store Name']]
# col_order_matters = True
# round_dec = 8

# output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
#               col_order_matters=col_order_matters, round_dec=round_dec)
