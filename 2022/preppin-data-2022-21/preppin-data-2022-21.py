# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 21 - Multi-sheets of Madness
https://preppindata.blogspot.com/2022/05/2022-week-21-multi-sheets-of-madness.html

- Connect to the data
- Bring together the Key Metrics tables from each Shop
- You'll notice that we have fields which report the quarter in addition to the monthly values. 
  We only wish to keep the monthly values
- Reshape the data so that we have a Date field
- For Orders and Returns, we are only interested in reporting % values, whilst for Complaints we 
  are only interested in the # Received
- We wish to update the Breakdown field to include the Department to make the Measure Name easier 
  to interpret
- We wish to have a field for each of the measures rather than a row per measure
- We wish to have the targets for each measure as field that we can compare each measure to
- Output the data

Author: Kelly Gilbert
Created: 2022-MM-DD
Requirements:
  - input dataset:
      - 2022W21 Input.xlsx
  - output dataset (for results check only):
      - 2022W21 Output.csv
"""


from numpy import where
import pandas as pd
from output_check import output_check


#---------------------------------------------------------------------------------------------------
# define constants
#---------------------------------------------------------------------------------------------------

# list of metrics to return
METRIC_LIST = ['% Shipped in 3 days', '% Shipped in 5 days', 
               '% Processed in 3 days', '% Processed in 5 days', 
               '# Received']


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in all of the sheets, copy the depts and targets down, remove unnecessary cols/rows
with pd.ExcelFile(r'.\inputs\2022W21 Input.xlsx') as xl:
    
    df = ( pd.concat([pd.read_excel(xl, sheet_name=s, skiprows=3, 
                                    usecols=lambda c: 'FY' not in str(c) and c != 'Comment')
                        .assign(Shop=s) 
                      for s in xl.sheet_names]) 
             .assign(Department=lambda df_x: df_x['Department'].ffill(),
                     Target=lambda df_x: df_x['Target'].ffill())
             .query(f"Breakdown == {str(METRIC_LIST)}")
         )    


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# melt the date columns into rows, convert targets to numbers, melt the targets/metrics into rows
df_out = ( df.melt(id_vars=['Shop', 'Department', 'Breakdown', 'Target'], 
                   var_name='Date', value_name='metric_value')
             .dropna() 
             .assign(Target=lambda df_x: df_x['Target'].astype(str))
             .assign(Target=lambda df_x: df_x['Target'].str.replace('[^0-9\.\-]', '', regex=True)
                                             .astype(float) 
                                             * where(df_x['Target'].str.contains('%'), 1/100, 1) )
             .melt(id_vars=['Shop', 'Department', 'Breakdown', 'Date'])
          )


# create the new column names
df_out['col_name'] = ( where(df_out['variable']=='Target', 'Target - ', '') 
                       + df_out['Breakdown'].str[0:2] + df_out['Department'] 
                       + ' ' + df_out['Breakdown'].str[2:] 
                     )

    
# pivot the metrics into columns
df_out = df_out.pivot_table(values='value', index=['Shop', 'Date'], 
                            columns=['col_name'], aggfunc='first').reset_index()


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-21.csv', index=False, date_format = '%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W21 Output.csv']
my_files = [r'.\outputs\output-2022-21.csv']
unique_cols = [['Shop', 'Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files, my_files, unique_cols, col_order_matters = False)
