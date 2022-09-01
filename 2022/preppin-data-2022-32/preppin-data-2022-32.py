# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 32 - C&BSCo Mortgage Repayments
https://preppindata.blogspot.com/2022/07/2022-week-32-c-mortgage-repayments.html

- Input the data
- Create a field for today (10th August 2022)
- Create a data field to show how much capital is paid off each month
- Create a data field to show how many months are needed to pay off the entire debt (whole months only)
- Create a field when the mortgages will be paid off by (Assuming a payment is to be made in August 2022)
- Create a row per month between now and when the mortgage is paid off showing:
- How much is still to be paid off for that mortgage? Call this field 'Remaining Capital to Repay'
- How much is still to be paid off for all mortgages? Call this field ' Capital Outstanding Total'
- Rename the date field 'Monthly Payment Date'
- Output the data

Author: Kelly Gilbert
Created: 2022-09-01
Requirements:
  - input dataset:
      - Preppin' Summer 2022 - Store Mortgages.csv
  - output dataset (for results check only):
      - PD 2022 Wk 32 Output.csv
"""


from datetime import datetime
from numpy import ceil
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


CURRENT_DATE = datetime(2022, 8, 10)


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r".\inputs\Preppin' Summer 2022 - Store Mortgages.csv")


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------


# monthly capital payment and months to pay off
df['Monthly Capital'] = df['Monthly Payment'] * df['% of Monthly Repayment going to Capital'] / 100

df['Months Remaining'] = ceil(df['Capital Repayment Remaining'] / df['Monthly Capital'])

df['Last Month'] = [CURRENT_DATE + pd.DateOffset(months=m-1) for m in df['Months Remaining']]


# create one row per month
df_out = ( df.assign(Monthly_Payment_Date = [pd.date_range(start=CURRENT_DATE, end=e, 
                                                           freq=pd.DateOffset(months=1)) 
                                             for e in df['Last Month']])
             .explode('Monthly_Payment_Date')
             .sort_values(by=['Store', 'Monthly_Payment_Date'])
             .rename(columns=lambda c: c.replace('_', ' '))
         )


# remaining capital by store and for all stores
df_out['Remaining Capital to Repay'] = ( df_out['Capital Repayment Remaining'] 
                                        - df_out.groupby('Store')['Monthly Capital'].transform('cumsum') )

df_out['Capital Outstanding Total'] = ( df_out.groupby('Monthly Payment Date')
                                            ['Remaining Capital to Repay'].transform('sum') )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Monthly Payment Date', 'Store', 'Capital Outstanding Total', 'Remaining Capital to Repay']
df_out.to_csv(r'.\outputs\output-2022-32.csv', index=False, columns=out_cols, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 32 Output.csv']
my_files = [r'.\outputs\output-2022-32.csv']
unique_cols = [['Store', 'Monthly Payment Date']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
