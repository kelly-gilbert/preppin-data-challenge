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
Created: 2020-07-18
Requirements: input dataset
  - PD week 12 input.xlsx
"""


from pandas import ExcelFile, read_csv, read_excel


# import and prep the plan data, starting on row 2
#    remove blank columns
#    trim column names
#    clean type
in_file = ExcelFile(r'.\inputs\PD week 12 input.xlsx')


# read in the Total Sales sheet
# convert the scent name to all caps, no spaces
df_tot = read_excel(in_file, sheet_name='Total Sales')
#df_tot.dtypes    # make sure numbers read in properly
df_tot.rename(columns={'Scent' : 'Scent_orig'}, inplace=True)
df_tot['Scent_join'] = df_tot['Scent_orig'].str.replace(' ', '')


# read in the Percentage of Sales sheet 
# get the year/week
# concatenate the Product ID and Size for joining to the lookup table
df_pct = read_excel(in_file, sheet_name='Percentage of Sales')
#df_pctsales.dtypes    # make sure numbers read in properly
df_pct['Product_join'] = df_pct['Product ID'] + df_pct['Size']
df_pct['Year Week Number'] = df_pct['Week Commencing'].dt.strftime('%Y%U').astype(int)
# I'm not sure what week-starting day to use, so I'm guessing Sunday
        

# read in the Lookup Table sheet and convert the scent to all caps, no spaces
df_lookup = read_excel(in_file, sheet_name='Lookup Table')
#df_lookup.dtypes    # make sure numbers read in properly
df_lookup['Scent_join'] = df_lookup['Scent'].str.upper().replace(' ', '')


# join the lookup data to the pct sales data
df = df_pct.merge(df_lookup, how='left', left_on='Product_join', right_on='Product')

# join the total sales data to the pct/lookup data
df = df.merge(df_tot, how='left', on=['Year Week Number', 'Scent_join'])


# check for unjoined data
# unjoined = df[df['Total Scent Sales'].isna()]
# unjoined.iloc[0]
#
# df_tot[df_tot['Scent_join']=='ORANGE']


# clean up the final table
df['Sales'] = df['Total Scent Sales'] * df['Percentage of Sales']
df = df[['Year Week Number', 'Scent', 'Size', 'Product Type', 'Sales']][df['Sales'].notna()]



df.iloc[0]

df.columns

df_tot.columns
df_pct.columns
df_lookup.columns

df.columns


# output to csv
df.to_csv('.\\outputs\\output-2020-12.csv', index=False, 
          columns=['Year Week Number', 'Scent', 'Size', 'Product Type', 'Sales'])




# check results
df_sol = read_csv('.\\outputs\\2020W12 Output - Fixed.csv')
df_sol.rename(columns={'Secnt' : 'Scent'}, inplace=True)

df2 = df_sol.merge(df, how='outer', on=['Year Week Number', 'Scent', 'Size', 'Product Type'])
df2[df2['Sales'].isna()]
