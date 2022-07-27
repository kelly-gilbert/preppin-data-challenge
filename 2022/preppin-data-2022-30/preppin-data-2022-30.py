# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 30 - C&BSCo Actual Sales Values
https://preppindata.blogspot.com/2022/07/2022-week-30-c-actual-sales-values.html

- Input the 'Top 3 Sales People per Store' for both regions: East & West
- Combine these files
  - Bonus challenge for experienced Preppers - take the Region Name from the File Name. For newer 
    Preppers, use the Region name field from the Week 27 Input later in the challenge
  - Input the 'Store Lookup' file to provide the name of the Stores instead of the ID number
- Remove any duplicate fields you have in the data set so far
- Input the Week 27 Input file
- Use Week 27 Input file to create Sales Values for each Store
- Combine this data with the rest of the prepared data
- Use the data set you have created to determine the actual sales value (rather than percentage) 
  for each sales person
  - Multiply the Sales Person percentage contribution against their Store's total sales for the year
- Output the data (removing any remaining duplicated fields)

Author: Kelly Gilbert
Created: 2022-07-27
Requirements:
  - input dataset:
      - Preppin_ Summer 2022 - PD 2022 Wk 27 Input.csv
      - Preppin_ Summer 2022 - Store Lookup.csv
      - Preppin_ Summer 2022 - Top 3 Sales People per Store (East).csv
      - Preppin_ Summer 2022 - Top 3 Sales People per Store (West).csv
  - output dataset (for results check only):
      - PD 2022 Wk 30 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in the regional top 3 files with bonus challenge
top3_filepaths = [r'.\inputs\Preppin_ Summer 2022 - Top 3 Sales People per Store (East).csv',
                  r'.\inputs\Preppin_ Summer 2022 - Top 3 Sales People per Store (West).csv']

df_top3 = pd.concat([pd.read_csv(f)
                       .assign(Region=f[f.find('(') + 1 : f.find(')')])
                     for f in top3_filepaths])

# read in the store lookup file
df_stores = pd.read_csv(r'.\inputs\Preppin_ Summer 2022 - Store Lookup.csv')

# read in the sales file, summarize by store
df_sales = ( pd.read_csv(r'.\inputs\Preppin_ Summer 2022 - PD 2022 Wk 27 Input.csv')
               .groupby('Store Name', as_index=False)['Sale Value'].sum()
           )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# replace the store ID with the store name
df_top3['Store Name'] = df_top3['Store'].replace({k:v for k,v in zip(df_stores['StoreID'], 
                                                                     df_stores['Store Name'])})


# combine sales and top3 sales person data
df_out = ( df_top3.merge(df_sales, on='Store Name', how='left')
                  .drop(columns='Store')
         )

# determine the actual sales value (rather than percentage) for each sales person
df_out['Sales per Person'] = df_out['Sale Value'] * df_out['Percent of Store Sales'] / 100


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-30.csv', index=False, 
              columns=['Sales per Person', 'Region', 'Store Name', 'Sales Person', 
                       'Percent of Store Sales', 'Sale Value'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 30 Output.csv']
my_files = [r'.\outputs\output-2022-30.csv']
unique_cols = [['Sales Person', 'Store Name']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
