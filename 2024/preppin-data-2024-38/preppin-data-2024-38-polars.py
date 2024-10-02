# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 38 - Preppin' Consultancy Days (polars)
https://preppindata.blogspot.com/2024/09/2024-week-38-preppin-consultancy-days.html

- Input all the worksheets in the Excel workbook
- Create an Initials field that has is formed as two letters. The Consultant Forename and Consultant Surname fields hold the details
  - i.e. Carl Allchin in the data is 3,1 we need CA
- Create an engagement start date and an engagement end date
  - The year is 2024 (in case you are doing this task after the normal release week)
- Clean up the Grade field by finding the minimum grade per person within the data set
  - Call this field 'Corrected Grade'
- Create an 'Engagement Order' based on the Engagement Start Date
- For each individual person (identified by unique initials), remove any engagements where the start date occurs before the previous Engagement End Date
- Join on the Grade details and remove the join clause fields
- Output the data

Author: Kelly Gilbert
Created: 2024-10-01
Requirements:
  - input dataset:
      - Preppin Data Consultancy.xlsx
  - output dataset (for results check only):
      - PD 2024 Wk 38 Output.csv
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

in_file = r'.\inputs\Preppin Data Consultancy.xlsx'
df_eng = pl.read_excel(in_file, sheet_name='Engagements')
df_init = pl.read_excel(in_file, sheet_name='Initials')
df_grade = pl.read_excel(in_file, sheet_name='Grade')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

initials_lookup = dict(zip(df_init['Initial ID'], df_init['Initial']))
df_out = (
    df_eng
     
        # form the initials and start/end dates 
        .with_columns(    
            (pl.col('Consultant Forename').cast(pl.String()).replace(initials_lookup)
                + pl.col('Consultant Surname').cast(pl.String()).replace(initials_lookup))
                .alias('Initials'),
            
            (pl.col('Engagement Start Month').cast(pl.String())
                + '/' + pl.col('Engagement Start Day').cast(pl.String())
                + '/2024') 
                .str.to_date('%m/%d/%Y')
                .alias('Engagement Start Date'),
        
            (pl.col('Engagement End Month').cast(pl.String())
                + '/' + pl.col('Engagement End Day').cast(pl.String())
                + '/2024') 
                .str.to_date('%m/%d/%Y')
                .alias('Engagement End Date')
        )
        
        .sort([pl.col('Engagement Start Date'), pl.col('Engagement End Date')])
        
        # order the engagements
        .with_columns( 
            pl.struct(pl.col('Engagement Start Date'), pl.col('Engagement End Date'))
                .rank(method='ordinal')
                .over(pl.col('Initials'))
                .alias('Engagement Order'),
            
            # add the prev end date for filtering
            pl.col('Engagement End Date') 
                .shift(1)
                .over('Initials')
                .alias('prev_end_date'),
                
            # add min grade per person                
            pl.col('Grade') 
                .min() 
                .over('Initials')
                .alias('Corrected Grade')
        )
        
        # remove records where the engagement start is > previous engagement end
        .filter((pl.col('Engagement Start Date') >= pl.col('prev_end_date'))
                | pl.col('prev_end_date').is_null())
        # .with_columns((pl.col('Engagement Start Date') >= pl.col('prev_end_date')).alias('filter'))
        
        # get grade attributes
        .join( 
            df_grade,
            left_on='Corrected Grade',
            right_on='Grade ID',
            how='left'
        )
)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Engagement Start Date', 'Engagement End Date', 'Initials', 'Engagement Order', 
            'Grade Name', 'Day Rate']

( df_out
    .select(out_cols)
    .write_csv(
        r'.\outputs\output-2024-38.csv', 
        date_format='%d/%m/%Y')
)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2024 Wk 38 Output.csv']
my_files = [r'.\outputs\output-2024-38.csv']
unique_cols = [['Initials', 'Engagement Order']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
