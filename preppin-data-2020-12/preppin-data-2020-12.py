# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-12
https://preppindata.blogspot.com/2020/03/2020-week-12.html
 
Cleaning messy data

- Input data
- Our final output requires the Date to be in in the Year Week Number format. 
- We don't care about any product sizes that make up 0% of sales.
- In the Lookup Table, it seems the Product ID and Size have been erroneously 
  concatenated. These need to be separated.  
- You'll need to do some cleaning of the Scent fields to join together the 
  Total Sales and the Lookup Table.
- Calculate the sales per week for each scent and product size.
- Output the data
- Output

Author: Kelly Gilbert
Created: 2020-07-17
Requirements: input dataset
  - PD week 12 input(1).xlsx
"""


from pandas import ExcelFile, read_csv, read_excel
import datetime as dt


def year_week_nbr(date_in):
    """
    mimic tableau week number
    if the year starts on sunday, use week number %U as-is, otherwise add one
    """
    if dt.date(date_in.year,1,1).weekday == 6:    # sunday
        adder=0
    else:
        adder=1       

    return date_in.year * 100 + int(dt.datetime.strftime(date_in, '%U')) + adder


#------------------------------------------------------------------------------
# import and prep the data
#------------------------------------------------------------------------------

in_file = ExcelFile(r'.\inputs\PD week 12 input(1).xlsx')


# Total Sales: convert the scent name to all caps, no spaces
df_tot = read_excel(in_file, sheet_name='Total Sales')
#df_tot.dtypes    # make sure numbers read in properly
df_tot.rename(columns={'Scent' : 'Scent_orig'}, inplace=True)
df_tot['Scent_join'] = df_tot['Scent_orig'].str.replace(' ', '')


# Percentage of Sales:
# get the year/week
# concatenate the Product ID and Size for joining to the lookup table
df_pct = read_excel(in_file, sheet_name='Percentage of Sales')
#df_pct.dtypes    # make sure numbers read in properly
df_pct = df_pct[df_pct['Percentage of Sales'] != 0]
df_pct['Product_join'] = df_pct['Product ID'] + df_pct['Size']
df_pct['Year Week Number'] = [year_week_nbr(d) for d in df_pct['Week Commencing']] 

# read in the Lookup Table sheet and convert the scent to all caps, no spaces
df_lookup = read_excel(in_file, sheet_name='Lookup Table')
#df_lookup.dtypes    # make sure numbers read in properly
df_lookup['Scent_join'] = df_lookup['Scent'].str.upper().replace(' +', '', regex=True)


#------------------------------------------------------------------------------
# merge (join) the data
#------------------------------------------------------------------------------

# join the lookup data to the pct sales data
df = df_pct.merge(df_lookup, how='left', left_on='Product_join', right_on='Product')

# join the total sales data to the pct/lookup data
df = df.merge(df_tot, how='left', on=['Year Week Number', 'Scent_join'])


# check for unjoined data (should be none)
# unjoined = df[df['Total Scent Sales'].isna()]
# unjoined.groupby(['Scent_join', 'Year Week Number'])['Year Week Number'].count()


# calculate sales and clean up the final table
df['Sales'] = round(df['Total Scent Sales'] * 100 * df['Percentage of Sales'], 0)/100
df = df[['Year Week Number', 'Scent', 'Size', 'Product Type', 'Sales']][df['Sales'].notna()]


# output to csv
df.to_csv('.\\outputs\\output-2020-12.csv', index=False, 
          columns=['Year Week Number', 'Scent', 'Size', 'Product Type', 'Sales'])


#------------------------------------------------------------------------------
# check results
#------------------------------------------------------------------------------

df_sol = read_csv('.\\outputs\\2020W12 Output - Fixed.csv')
df_sol.rename(columns={'Secnt' : 'Scent'}, inplace=True)

df_check = df_sol.merge(df, suffixes=['_sol','_mine'], how='outer', 
                        on=['Year Week Number', 'Scent', 'Size', 'Product Type'])


print('In solution, not in mine:')
unmatched = df_check[df_check['Sales_sol'].isna()]
if len(unmatched)==0:
    print('Nothing')
else:
    print(unmatched)


print('\nIn mine, not in solution:')
unmatched = df_check[df_check['Sales_mine'].isna()]
if len(unmatched)==0:
    print('Nothing')
else:
    print(unmatched)


print('\nSales value does not match:')
unmatched = df_check[df_check['Sales_sol'] != df_check['Sales_mine']]
if len(unmatched)==0:
    print('Nothing')
else:
    print(unmatched)

#df[(df['Year Week Number']==202003) & (df['Scent']=='Mint') & (df['Size']=='100g')].iloc[0]
#df_sol[(df_sol['Year Week Number']==202003) & (df_sol['Scent']=='Mint') & (df_sol['Size']=='100g')].iloc[0]