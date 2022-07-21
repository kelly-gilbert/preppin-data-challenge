# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 23 - PD x WOW Salesforce Opportunities
https://preppindata.blogspot.com/2022/06/2022-week-23-pd-x-wow-salesforce.html

- Input the data
- For the Opportunity table:
  - Pivot the CreatedDate & CloseDate fields so that we have a row for when each opportunity Opened
    and a row for the ExpectedCloseDate of each opportunity
    - Rename the Pivot 1 Values field to Date 
    - Rename the Pivot 1 Names field to Stage and update the values
  - Update the Stage field so that if the opportunity has closed (see the StageName field) the 
    ExpectedCloseDate is updated with the StageName
  - Remove unnecessary fields
    - Hint: look at the fields in common with the Opportunity History table
- Bring in the additional information from the Opportunity History table about when each opportunity
  moved between each stage
- Ensure each row has a SortOrder associated with it
  - Opened rows should have a SortOrder of 0
  - ExpectedCloseDate rows should have a SortOrder of 11
- Remove unnecessary fields
- Remove duplicate rows that may have occurred when brining together the two tables
- Output the data 

Author: Kelly Gilbert
Created: 2022-07-18
Requirements:
  - input dataset:
      - Opportunity.csv
      - Opportunity History.csv
  - output dataset (for results check only):
      - Cleaned Salesforce Data.csv
"""


from numpy import where
import pandas as pd
from output_check import output_check    # custom function for comparing my results to the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\Opportunity.csv', parse_dates=['CreatedDate', 'CloseDate'], dayfirst=True)
df_hist = pd.read_csv(r'.\inputs\Opportunity History.csv', parse_dates=['CreatedDate'], dayfirst=True)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# stack the open dates, expected close dates, and history
df_out = pd.concat([df[['Id', 'CreatedDate']]
                        .assign(Stage='Opened', 
                                SortOrder=0),
                    df[~df['StageName'].str.contains('Closed')][['Id', 'CloseDate']]
                        .assign(Stage='ExpectedCloseDate',
                                SortOrder=11),
                    df_hist.rename(columns={'StageName' : 'Stage'})])


# combine the date
df_out['Date'] = where(df_out['CreatedDate'].notna(), df_out['CreatedDate'], df_out['CloseDate'])


# combine the IDs
df_out['OppID'] = where(df_out['OppID'].notna(), df_out['OppID'], df_out['Id'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-23.csv', index=False, date_format='%d/%m/%Y', 
              columns=['OppID', 'Date', 'Stage', 'SortOrder'])


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Cleaned Salesforce Data.csv']
my_files = [r'.\outputs\output-2022-23.csv']
unique_cols = [['OppID', 'Date', 'Stage']]
col_order_matters = False
round_dec = 2

output_check(solution_files, my_files, unique_cols, col_order_matters = False)






#---------------------------------------------------------------------------------------------------
# options for creating the open/close date records
#---------------------------------------------------------------------------------------------------

# option 1 - melt the open and closed dates, remove any that are already closed
# 3.66 s ± 357 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) -- original df x 5000 (1.1 M) 
# prettier code, but much slower

%%timeit 
df_melt = ( df.melt(id_vars=['Id', 'StageName'], value_vars=['CloseDate', 'CreatedDate'], 
                    value_name='Date', var_name='StageName2')
              .query('~(StageName.str.contains("Closed").values & StageName2=="CloseDate")')
              .drop(columns='StageName')
              .rename(columns={'StageName2' : 'Stage'})
              .assign(Stage=lambda df_x: where(df_x['Stage']=='CloseDate',
                                               'ExpectedCloseDate', 'Opened'))
          )


# option 2 - slice the dataframe into open and closed, then concatenate them -- FASTER
# 689 ms ± 15.5 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) -- original df x 5000 (1.1 M) 

%%timeit 
df_melt = ( pd.concat([df[['Id', 'CreatedDate']]
                          .assign(Stage='Opened',
                                  SortOrder=0)
                          .rename(columns={'CreatedDate' : 'Date', 'Id' : 'OppID', }),
                      df[~df['StageName'].str.contains('Closed')][['Id', 'CloseDate']]
                          .assign(Stage='ExpectedCloseDate')
                          .rename(columns={'CloseDate' : 'Date', 'Id' : 'OppID'}) ])
         )


#---------------------------------------------------------------------------------------------------
# options for handling the renames and calcs
#---------------------------------------------------------------------------------------------------

# option 1 - handle renames and calculations in chain
# 700 ms ± 38.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) -- FASTER
# original df x 5000 (1.1 M recs)

%%timeit 
df_out = ( pd.concat([df[['Id', 'CreatedDate']].assign(Stage='Opened',
                                  SortOrder=0)
                          .rename(columns={'CreatedDate' : 'Date', 'Id' : 'OppID', }),
                      df[~df['StageName'].str.contains('Closed')][['Id', 'CloseDate']]
                          .assign(Stage='ExpectedCloseDate', SortOrder=11)
                          .rename(columns={'CloseDate' : 'Date', 'Id' : 'OppID'}),
                      df_hist.rename(columns={'CreatedDate' : 'Date', 'StageName' : 'Stage'})])
          )



# option 2 - handle renames and calculations in series
# 1.64 s ± 25.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# original df x 5000 (1.1 M recs)

%%timeit 
# stack the open dates, expected close dates, and history
df_out = pd.concat([df[['Id', 'CreatedDate']],
                    df[~df['StageName'].str.contains('Closed')][['Id', 'CloseDate']],
                    df_hist])

# add the stage name
df_out['Stage'] = where(df_out['StageName'].notna(), 
                        df_out['StageName'], 
                        where(df_out['CloseDate'].isna(), 'Opened', 'ExpectedCloseDate'))

# add the date
df_out['Date'] = where(df_out['CreatedDate'].notna(), df_out['CreatedDate'], df_out['CloseDate'])


# combine the IDs
df_out['OppID'] = where(df_out['OppID'].notna(), df_out['OppID'], df_out['Id'])


# add the sort order
df_out['SortOrder'] = where(df_out['SortOrder'].notna(), 
                            df_out['SortOrder'], 
                            df_out['Stage'].replace({'Opened' : 0, 'ExpectedCloseDate' : 11}))



# option 3 - assign in chain, manage dates/ID separately
# 799 ms ± 25.2 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# original df x 5000 (1.1 M recs)
 
%%timeit 
# stack the open dates, expected close dates, and history
df_out = pd.concat([df[['Id', 'CreatedDate']]
                        .assign(Stage='Opened', 
                                SortOrder=0),
                    df[~df['StageName'].str.contains('Closed')][['Id', 'CloseDate']]
                        .assign(Stage='ExpectedCloseDate',
                                SortOrder=11),
                    df_hist.rename(columns={'StageName' : 'Stage'})])


# combine the date
df_out['Date'] = where(df_out['CreatedDate'].notna(), df_out['CreatedDate'], df_out['CloseDate'])


# combine the IDs
df_out['OppID'] = where(df_out['OppID'].notna(), df_out['OppID'], df_out['Id'])


