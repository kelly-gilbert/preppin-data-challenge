# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 03 - Targets for DSB
https://preppindata.blogspot.com/2023/01/2023-week-3-targets-for-dsb.html

- Input the data
- For the transactions file:
  - Filter the transactions to just look at DSB
    - These will be transactions that contain DSB in the Transaction Code field
  - Rename the values in the Online or In-person field, Online of the 1 values and In-Person for the 2 values
  - Change the date to be the quarter
  - Sum the transaction values for each quarter and for each Type of Transaction (Online or In-Person)
- For the targets file:
  - Pivot the quarterly targets so we have a row for each Type of Transaction and each Quarter
  - Rename the fields
  - Remove the 'Q' from the quarter field and make the data type numeric
- Join the two datasets together
  - You may need more than one join clause!
- Remove unnecessary fields
- Calculate the Variance to Target for each row
- Output the data

Author: Kelly Gilbert
Created: 2023-04-15
Requirements:
  - input dataset:
      - PD 2023 Wk 1 Input.csv
      - Targets.csv
  - output dataset (for results check only):
      - None (checked by visual inspection this week)
"""


import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# read in the transactions and filter for DSB
df = ( pd.read_csv(r'.\inputs\PD 2023 Wk 1 Input.csv')
         .query("`Transaction Code`.str.contains('DSB')", engine='python') )


# read in the targets and melt quarters into rows
df_t = ( pd.read_csv(r'.\inputs\Targets.csv')
           .melt(id_vars='Online or In-Person', 
                 var_name='Quarter',
                 value_name='Quarterly Targets')
           .assign(Quarter = lambda df_x: df_x['Quarter'].str.replace('Q', '').astype(int)) )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# replace the type codes with labels
type_codes = { 1 : 'Online',
               2 : 'In-Person'}
df['Online or In-Person'] = df['Online or In-Person'].replace(type_codes).astype('category')


# convert date to quarter
df['Quarter'] = pd.to_datetime(df['Transaction Date'], dayfirst=True).dt.quarter


# sum the transaction values by type and quarter and compare to targets
df_out = ( df.groupby(['Online or In-Person', 'Quarter'], as_index=False)['Value'].sum()
             .merge(df_t,
                    on=['Online or In-Person', 'Quarter'],
                    how='left') )

df_out['Variance to Target'] = df_out['Value'] - df_out['Quarterly Targets']


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2023-03.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection
print(pd.read_csv(r'.\outputs\output-2023-03.csv'))
