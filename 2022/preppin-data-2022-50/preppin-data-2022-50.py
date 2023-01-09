# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 50 - Withdrawals (HR month)
https://preppindata.blogspot.com/2022/12/2022-week-50-withdrawals-hr-month.html

- Input the data
- Rank the statuses based on the timestamp (ts) field, where the most recent status is 1
- If the most recent status (rank #1) is “Candidate Withdrew”, find the previous status (rank #2)
- Count the number of withdrawals, grouped by the previous status
- Count the total number of candidate/positions that have ever been in each status
- Join the total counts by status to the withdrawals by status
  - Make sure that statuses with no withdrawals are included in the output
- Calculate the % of candidates who withdrew after each status (round to 1 decimal place, e.g. output “2.5” for 2.5%)
- Clean up the columns so four columns remain:
  - status_before_withdrawal
  - total_candidates
  - withdrawals
  - Pct_withdrawn

Author: Kelly Gilbert
Created: 2022-01-06
Requirements:
  - input dataset:
      - status_history_clean.csv
  - output dataset (for results check only):
      - withdrawals_by_status.csv
"""


from numpy import where
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


# --------------------------------------------------------------------------------------------------
# import the data
# --------------------------------------------------------------------------------------------------

df = ( pd.read_csv(r'.\inputs\status_history_clean.csv', parse_dates=['ts'], dayfirst=True)
         .sort_values(by='ts') )


# --------------------------------------------------------------------------------------------------
# process the data
# --------------------------------------------------------------------------------------------------

# flag if the next status is withdrew
df['withdrew_flag'] = where(df.groupby(['candidate_id','position_id'])['status'].shift(-1) \
                                == 'Candidate Withdrew',
                            1, 0)

# summarize
df_out = ( df.groupby('status', as_index=False).agg(withdrawals=('withdrew_flag', 'sum'),
                                                    total_in_status=('candidate_id', 'count'))
             .rename(columns={'status' : 'status_before_withdrawal' }) )

df_out['pct_withdrawn'] = round(df_out['withdrawals'] / df_out['total_in_status'] * 100, 1)


# --------------------------------------------------------------------------------------------------
# output the data
# --------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2022-50.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\withdrawals_by_status.csv']
my_files = [r'.\outputs\output-2022-50.csv']
unique_cols = [['status_before_withdrawal']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
