# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 03 - Targets for DSB (Polars solution)
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
Created: 2023-06-17
Requirements:
  - input dataset:
      - PD 2023 Wk 1 Input.csv
      - Targets.csv
  - output dataset (for results check only):
      - None (checked by visual inspection this week)
"""


import polars as pl


#---------------------------------------------------------------------------------------------------
# input and prep the datasets
#---------------------------------------------------------------------------------------------------

LOCATION_RENAMES = { 1 : 'Online',
                     2 : 'In-Person' }


# read in, filter, and update the transaction data, group by location and quarter
df = ( pl.read_csv(r'.\inputs\PD 2023 Wk 1 Input.csv', 
                   try_parse_dates=True)
      
         # read in the transactions and filter for DSB
         .filter(pl.col('Transaction Code').str.contains('DSB'))
         
         # change the date to quarter and replace the location codes
         .with_columns(
             [ pl.col('Transaction Date').dt.quarter()
                 .cast(pl.Int8)
                 .alias('Quarter'),
               pl.col('Online or In-Person').map_dict(LOCATION_RENAMES, 
                                                      default=pl.col('Online or In-Person'))
             ]
         )
         
         # group by location and quarter
         .groupby(['Online or In-Person', 'Quarter'])
         .agg(pl.col('Value').sum())
      )


# read in the targets and melt quarters into rows
df_t = ( pl.read_csv(r'.\inputs\Targets.csv')
           .melt(id_vars='Online or In-Person', 
                 variable_name='Quarter',
                 value_name='Quarterly Targets')
           .with_columns(pl.col('Quarter').str.replace('Q', '', literal=True)
                                          .cast(pl.Int8)) )


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df_out = ( df.join(df_t,
                   on=['Online or In-Person', 'Quarter'],
                   how='left')
             .with_columns( (pl.col('Value') - pl.col('Quarterly Targets'))
                            .alias('Variance to Target')
             )
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.write_csv(r'.\outputs\output-2023-03.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection
print(pl.read_csv(r'.\outputs\output-2023-03.csv'))
