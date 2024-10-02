# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 38 - Preppin' Consultancy Days
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
Created: 2024-09-28
Requirements:
  - input dataset:
      - Preppin Data Consultancy.xlsx
  - output dataset (for results check only):
      - PD 2024 Wk 38 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\Preppin Data Consultancy.xlsx') as xl:
    df_eng = pd.read_excel(xl, sheet_name='Engagements')
    df_init = pd.read_excel(xl, sheet_name='Initials')
    df_grade = pd.read_excel(xl, sheet_name='Grade')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

initials_lookup = dict(zip(df_init['Initial ID'], df_init['Initial']))

df_out = (
    df_eng
     
        # form the initials and start/end dates 
        .assign(    
            Initials = lambda df_x: ( 
                df_x['Consultant Forename'].replace(initials_lookup).astype(str)
                    + df_x['Consultant Surname'].replace(initials_lookup)).astype(str),
            Engagement_Start_Date = lambda df_x: pd.to_datetime(
                df_x['Engagement Start Month'].astype(str) 
                    + '/' + df_x['Engagement Start Day'].astype(str) 
                    + '/2024',
                dayfirst=False),
            Engagement_End_Date = lambda df_x: pd.to_datetime(
                df_x['Engagement End Month'].astype(str) 
                    + '/' + df_x['Engagement End Day'].astype(str) 
                    + '/2024',
                dayfirst=False)
        ) 
        
        # order the engagements, add the prev end date for filtering, and add min grade per person
        .assign(
            Engagement_Order = lambda df_x: \
                df_x
                    .sort_values(['Engagement_Start_Date', 'Engagement_End_Date']) 
                    .groupby('Initials')
                    ['Engagement_Start_Date'].rank(method='first').astype(int),
                
            prev_end_date = lambda df_x: \
                df_x
                    .sort_values(['Engagement_Start_Date', 'Engagement_End_Date'])
                    .groupby('Initials')
                    ['Engagement_End_Date'].shift(1),
            
            Corrected_Grade = lambda df_x : \
                df_x.groupby('Initials')['Grade'].transform('min')
        )
        
        # get grade attributes
        .merge(
            df_grade,
            left_on='Corrected_Grade',
            right_on='Grade ID',
            how='left'
        ) 
        
        # remove records where the engagement start is > previous engagement end
        .query("Engagement_Start_Date >= prev_end_date.fillna('1900-01-01')")
        
        # clean up column names
        .rename(columns=lambda c: c.replace('_', ' '))
    )
   

#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Engagement Start Date', 'Engagement End Date', 'Initials', 'Engagement Order', 
            'Grade Name', 'Day Rate']

df_out.to_csv(r'.\outputs\output-2024-38.csv', 
              index=False, 
              columns=out_cols,
              date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2024 Wk 38 Output.csv']
my_files = [r'.\outputs\output-2024-38.csv']
unique_cols = [['Initials', 'Engagement Start Date', 'Engagement End Date']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
