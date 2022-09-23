# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 38 - Salesforce Standard Connections for Dreamforce22
https://preppindata.blogspot.com/2022/09/2022-week-38-salesforce-standard.html

- Connect to Salesforce within Tableau Prep (or to the input files)
- Recreate the Opportunities Standard Connection (see above)
- Only include the fields listed above
- Output the data
- Now we want to create datasets which will easily answer some questions:
  - Who is the Opportunity Owner with the Highest Amount?
  - Who is the Account Owner with the Highest Amount?
  - Which Account has the most Opportunities & Amount?
- Create an output for each question

Author: Kelly Gilbert
Created: 2022-09-22
Requirements:
  - input datasets:
      - Opportunity.csv
      - Account.csv
      - User.csv
  - output dataset (for results check only):
      - Opportunities Standard Connection.csv
      - Highest Amount Opportunity Owner.csv
      - Highest Amount Account Owner.csv
      - Account Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_opp =( pd.read_csv(r'.\inputs\Opportunity.csv', 
                      usecols=['Id', 'Name', 'AccountId', 'StageName', 'Amount', 'OwnerId', 'CreatedById'])
            .rename(columns={'Id' : 'Opportunity ID',
                             'Name' : 'Opportunity Name'}) )

df_acc = ( pd.read_csv(r'.\inputs\Account.csv', 
                       usecols=['Id', 'Name', 'Type', 'CreatedById', 'OwnerId'])
             .rename(columns=lambda c: f"Account{'' if 'Id' in c else ' '}{c}") )

df_user = pd.read_csv(r'.\inputs\User.csv', usecols=['Id', 'Name', ])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# add account info to the opportunity info
df_out = df_opp.merge(df_acc, on='AccountId', how='left')


# add the user names
users = dict(zip(df_user['Id'], df_user['Name']))
df_out['Created By Name'] = df_out['CreatedById'].replace(users)
df_out['Owner Name'] = df_out['OwnerId'].replace(users)
df_out['Account Created By Name'] = df_out['AccountCreatedById'].replace(users)
df_out['Account Owner Name'] = df_out['AccountOwnerId'].replace(users)


# remove unnecessary fields
df_out = df_out.drop(columns=['AccountCreatedById', 'AccountOwnerId'])


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

# output the opportunities standard connection data
df_out.to_csv(r'.\outputs\output-2022-38-opportunities-standard-connection.csv', index=False)


#---------------------------------------------------------------------------------------------------
# questions
#---------------------------------------------------------------------------------------------------

# 1 - who is the opportunity owner with the highest amount?
( df_out.groupby('Owner Name', as_index=False)['Amount'].sum()
        .sort_values(by='Amount', ascending=False)
        .to_csv(r'.\outputs\output-2022-38-highest-amount-opportunity-owner.csv', index=False) )


# 2 - who is the account owner with the highest amount?
( df_out.groupby('Account Owner Name', as_index=False)['Amount'].sum()
        .sort_values(by='Amount', ascending=False)
        .to_csv(r'.\outputs\output-2022-38-highest-amount-account-owner.csv', index=False) )


# 3 - which account has the most opportunities & amount?
( df_out.groupby('Account Name', as_index=False).agg(Number_of_Opportunities = ('Opportunity ID', 'count'),
                                                     Amount=('Amount', 'sum'))
        .rename(columns=lambda c: c.replace('_', ' '))
        .to_csv(r'.\outputs\output-2022-38-account-output.csv', index=False) )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Opportunities Standard Connection.csv', 
                  r'.\outputs\Highest Amount Opportunity Owner.csv', 
                  r'.\outputs\Highest Amount Account Owner.csv', 
                  r'.\outputs\Account Output.csv']
my_files = [r'.\outputs\output-2022-38-opportunities-standard-connection.csv',
            r'.\outputs\output-2022-38-highest-amount-opportunity-owner.csv',
            r'.\outputs\output-2022-38-highest-amount-account-owner.csv',
            r'.\outputs\output-2022-38-account-output.csv']
unique_cols = [['Opportunity Name', 'AccountId'],
               ['Owner Name'],
               ['Account Owner Name'],
               ['Account Name']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
