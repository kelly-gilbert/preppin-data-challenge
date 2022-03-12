# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 09 - Customer Classifications
https://preppindata.blogspot.com/2022/03/2022-week-9-customer-classifications.html

- Input the data
- Aggregate the data to the years each customer made an order
- Calculate the year each customer made their First Purchase
- Scaffold the dataset so that there is a row for each year after a customers First Purchase, even 
  if they did not make an order
- Create a field to flag these new rows, making it clear whether a customer placed an order in that 
  year or not
- Calculate the Year on Year difference in the number of customers from each Cohort in each year
    - Cohort = Year of First Purchase
- Create a field which flags whether or not a customer placed an order in the previous year
- Create the Customer Classification using the above definitions
- Join back to the original input data
    - Ensure that in rows where a customer did not place an order, the majority of the original 
      fields are null. The exceptions to this are the Customer Name and Customer Name fields.
- Output the data

Author: Kelly Gilbert
Created: 2022-03-10
Requirements:
  - input dataset:
      - Sample - Superstore.xls
  - output dataset (for results check only):
      - Customer Classification Output.csv
"""

from numpy import nan, where
import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_excel(r'.\inputs\Sample - Superstore.xls', 'Orders')\
       .assign(Year=df['Order Date'].dt.year)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# generate a list of all possible customer/year combos
# join to the actual cust/year combos
# set Order flag
# remove years before the first purchase
df_cust_yr = df.groupby(['Customer ID', 'Customer Name'], as_index=False).agg(First_Purchase=('Year', 'min'))\
               .merge(pd.DataFrame({'Year':df['Year'].unique()}), how='cross')\
               .merge(df.groupby(['Customer ID', 'Year']).agg(Order_Lines=('Row ID', 'count')), 
                      on=['Customer ID', 'Year'], how='left')\
               .assign(Order_flag=lambda df_x: where(df_x['Order_Lines'].isna(), 0, 1))\
               .drop(columns='Order_Lines')\
               .query('Year >= First_Purchase')\
               .sort_values(by=['Customer ID', 'Year'])\
               .rename(columns={'Order_flag' : 'Order?', 'First_Purchase' : 'First Purchase'})
       
# add the classification        
df_cust_yr['Customer Classification'] = \
    where(df_cust_yr['Order?'] == 0, 'Sleeping',
        where(df_cust_yr['Year'] == df_cust_yr['First Purchase'], 'New',
            where(df_cust_yr['Order?'].shift(1) == 0, 'Returning', 'Consistent'))) 

# calculate YoY change in number of customers
df_cust_yr['YoY Difference'] = \
    where(df_cust_yr['Customer Classification']=='New', nan,
        (df_cust_yr.groupby(['Year', 'First Purchase'])['Order?'].transform('sum') \
         - df_cust_yr.groupby(['Year', 'First Purchase'])['Order?'].transform('sum').shift(1))\
        .astype('Int16'))


# add the new fields back to the main data
df_out = df.merge(df_cust_yr, on=['Customer ID', 'Customer Name', 'Year'], how='right')
                  

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-09.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['Customer Classification Output.csv']
my_files = ['output-2022-09.csv']
unique_cols = [['Customer ID', 'Year', 'Row ID']]
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
                                   & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])
                                   & ((df_compare[f'{c}_sol'].notna()) 
                                      | (df_compare[f'{c}_mine'].notna()))]
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
    

# --------------------------------------------------------------------------------------------------
# performance testing
# --------------------------------------------------------------------------------------------------

# methods for creating all possible customer/year combinations
# method 2 takes ~40% less time

# method 1 (slower): drop duplicates
%%timeit 
df_cust_yr = df[['Customer Name']].drop_duplicates()\
               .merge(df[['Year']].drop_duplicates(), how='cross')

# method 2 (faster): create dataframes from unique values
%%timeit 
df_cust_yr = pd.DataFrame({'Customer Name':df['Customer Name'].unique()})\
                       .merge(pd.DataFrame({'Year':df['Year'].unique()}), how='cross')



# get all existing combos of customer/year
# method 1 is ~30% faster
               
# method 1 (FASTER): drop duplicates
%timeit df[['Customer Name', 'Year']].drop_duplicates()

# method 2 (SLOWER): groupby with a throwaway aggregation
%timeit df.groupby(['Customer Name', 'Year'], as_index=False)['Year'].size()
               .query('Year >= First_Purchase')



# generate the df_cust_yr dataframe
# method 1 is about half the time of method 2
               
# method 1 (FASTER): method used in the script above
%%timeit 
df_cust_yr = pd.DataFrame({'Customer Name' : df['Customer Name'].unique()})\
               .merge(pd.DataFrame({'Year':df['Year'].unique()}), how='cross')\
               .merge(df.groupby(['Customer Name', 'Year']).agg(First_Purchase=('Year', 'min')), 
                      on=['Customer Name', 'Year'], how='left')\
               .assign(Order_flag=lambda df_x: where(df_x['First_Purchase'].isna(), 0, 1),
                       First_Purchase=lambda df_x: df_x.groupby(['Customer Name'])['First_Purchase']\
                                                       .transform('min'))\
               .query('Year >= First_Purchase')
               
# method 2 (SLOWER): create list of valid years and explode instead of cross joining/query
%%timeit 
df_cust_yr = df.groupby('Customer Name').agg(First_Purchase=('Year', 'min'))\
               .assign(Year=lambda df_x: [range(f, df['Year'].max() + 1) for f in df_x['First_Purchase']])\
               .explode('Year')\
               .merge(df.groupby(['Customer Name', 'Year'])['Order ID'].count(), 
                      on=['Customer Name', 'Year'], how='left')\
               .drop(columns='Order ID')\
               .assign(Order_flag=lambda df_x: where(df_x['First_Purchase'].isna(), 0, 1),
                       First_Purchase=lambda df_x: df_x.groupby(['Customer Name'])['First_Purchase']\
                                                       .transform('min'))
                   
