# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 51 - Parsing an Unfortunate Report Format (HR Month)
https://preppindata.blogspot.com/2022/12/2022-week-51-parsing-unfortunate-report.html

- Input the data
- Remove the header rows (row 1 and year headers)
- Parse five fields from each row: 
  - Application Month
  - Work Experience
  - Number Supervised
  - Industry Experience
- Candidate Count (the number in parentheses)
- Remove blank columns and the original data column
- Convert the application month to the month-ending date
- For each month, calculate the % of applicants who meet the preferred qualifications.
  - Preferred qualifications are:
    - Work Experience: at least 4 years
    - Number Supervised: more than 10
    - Industry Experience: Yes
  - Flag the rows that meet all of the preferred calculations
  - For each month, sum the total number of applicants and the number meeting the preferred qualifications
  - Calculate the % who met the preferred qualifications. Output the % with one decimal place (e.g. 10.2% = “10.2”)
- Output the data

Author: Kelly Gilbert
Created: 2023-01-09
Requirements:
  - input dataset:
      - application_report.xlsx
"""


from numpy import where
import pandas as pd


# --------------------------------------------------------------------------------------------------
# import the data
# --------------------------------------------------------------------------------------------------

# keep only the 2nd column
df = pd.read_excel(r'.\inputs\application_report.xlsx', 
                   header=None, skiprows=1, 
                   usecols=[1], names=['data'])


# --------------------------------------------------------------------------------------------------
# process the data
# --------------------------------------------------------------------------------------------------

# ---------- simple method (hard-code column names) ----------

# df_parsed = df['data'].str.extract('Application Date: (.*), Work Experience: (.*), Supervised: (.*),'\
#                                    ' Industry Experience: (.*) \((\d+)\)')
# df_parsed.columns = ['application_month', 'work_experience', 'supervised', 'industry_experience', 
#                      'candidate_count']
# df_parsed = df_parsed.loc[df_parsed['candidate_count'].notna(), :]


# -- OR -- 


# ---------- dynamic method (can handle different questions/number of questions) ----------

# parse the question/answer pairs into rows, then parse the questions and answers, put questions into cols
df_parsed = ( df['data'].str.extractall('\s*(.*?)\s*(?:,|\(|\))')[0]
                        .str.extract('(?P<question>.*?(?=:))?(?:\:\s)?(?P<answer>.*)')
                        .reset_index() )

df_parsed['question'] = where(df_parsed['question'].isna() & df_parsed['answer'].notna(), 
                              'candidate_count', 
                              df_parsed['question'].str.lower().str.replace(' ', '_', regex=False) )

df_parsed = ( pd.pivot_table(df_parsed, 
                             values='answer', index='level_0', columns='question', 
                             aggfunc='first')
                .query('application_date.str.len() > 4')
                .reset_index(drop=True) )



# flag preferred criteria and summarize
df_parsed['candidate_count'] = df_parsed['candidate_count'].astype(int)

df_parsed['preferred_count'] = where((~df_parsed['work_experience'].isin(['0-3 years']))
                                     & (~df_parsed['supervised'].isin(['None', '1-5', '6-10']))
                                     & (df_parsed['industry_experience'] == 'Yes'),
                                     df_parsed['candidate_count'].astype(int), 0)

df_out = ( df_parsed.groupby('application_date', as_index=False)
                    .agg(preferred_count = ('preferred_count', 'sum'),
                                            total_count = ('candidate_count', 'sum')) )

df_out['pct_meeting_preferred'] = round(df_out['preferred_count'] / df_out['total_count'] * 100, 1)



# convert the application month/year to EOM date
df_out['application_date'] = (pd.to_datetime(df_out['application_date']) 
                              + pd.DateOffset(months=1) 
                              - pd.DateOffset(days=1) )


# --------------------------------------------------------------------------------------------------
# output the data
# --------------------------------------------------------------------------------------------------

renames = { 'application_date' : 'Application Month',
            'total_count' : 'Total Candidates',
            'preferred_count' : 'Candidates with Preferred Qualifications',
            'pct_meeting_preferred' : '% of Candidates' }

df_out.rename(columns=renames)\
      .to_csv(r'.\outputs\output-2022-51.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection


df_out.rename(columns=renames).sort_values('Application Month')
