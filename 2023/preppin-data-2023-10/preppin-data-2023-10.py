# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 10 - What's my balance on this day? (polars)
https://preppindata.blogspot.com/2023/03/2023-week-10-whats-my-balance-on-this.html

- Input the data
- Aggregate the data so we have a single balance for each day already in the dataset, for each account
- Scaffold the data so each account has a row between 31st Jan and 14th Feb (hint)
- Make sure new rows have a null in the Transaction Value field
- Create a parameter so a particular date can be selected
- Filter to just this date
- Output the data - making it clear which date is being filtered to

Author: Kelly Gilbert
Created: 2023-06-26
Requirements:
  - input dataset:
      - Account Statements.csv
  - output dataset (for results check only):
      - Balance as of 2023-02-01.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

start_date = pd.to_datetime('2023-01-31')
end_date = pd.to_datetime('2023-02-14')


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input the csv and keep one record per date
df = ( pd.read_csv(r'.\inputs\Account Statements.csv', 
                   parse_dates=['Balance Date'], dayfirst=True)
         .sort_values(by=['Account Number', 'Balance Date', 'Transaction Value'],
                      ascending=[True, True, False])
         .groupby(['Account Number', 'Balance Date'], as_index=False)
         .agg(Transaction_Value = ('Transaction Value', 'sum'),
              Balance = ('Balance', 'last'))
         .rename(columns=lambda c: c.replace('_', ' '))
     )
         

#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create all combos of account number/balance date, then join to actual data
df_out = ( df[['Account Number']].drop_duplicates()
              .merge(pd.DataFrame({ 'Balance Date' : pd.date_range(start_date,
                                                                   end_date,
                                                                   freq='1D')}),
                    how='cross')
              .merge(df,
                     on=['Account Number', 'Balance Date'],
                     how='left')
              .assign(Balance = lambda df_x: df_x.groupby('Account Number')['Balance'].ffill())
         )


#---------------------------------------------------------------------------------------------------
# get user input and output the file
#---------------------------------------------------------------------------------------------------

while (user_input := input('Enter the balance date (yyyy-mm-dd format) or Enter to cancel:')) != '':
    user_ts = pd.to_datetime(user_input, errors='coerce')
    
    if not isinstance(user_ts, pd.Timestamp):
        print(chr(10) + r'Please enter a valid date in yyyy-mm-dd format.', end=chr(10)*2)
        
    elif user_ts < start_date or user_ts > end_date:
        print(chr(10) + f'Please enter a date between {str(start_date)[0:10]} '\
              + f'and {str(end_date)[0:10]}.', end=chr(10)*2)
    else:
        filename = fr'.\outputs\Balance as of {str(user_ts)[0:10]}_klg.csv'
        ( df_out[df_out['Balance Date']==user_ts]
             [['Account Number', 'Transaction Value', 'Balance']]
             .to_csv(filename, index=False)
        )
       
        print(chr(10) + f"Data was output to '{filename}'", end=chr(10)*2)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Balance as of 2023-02-01.csv']
my_files = [r'.\outputs\Balance as of 2023-02-01_klg.csv']
unique_cols = [['Account Number']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)


#---------------------------------------------------------------------------------------------------
# timing different methods of filling in the missing dates
#---------------------------------------------------------------------------------------------------

# create all combos of account number/balance date, then join to actual data -- FASTER
# 43 ms ± 249 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
df_out = ( df[['Account Number']]
              .merge(pd.DataFrame({ 'Balance Date' : pd.date_range(df['Balance Date'].min(),
                                                                   df['Balance Date'].max(),
                                                                   freq='1D')}),
                    how='cross')
              .merge(df,
                     on=['Account Number', 'Balance Date'],
                     how='left')
         )


# method 2 - multiindex -- SLOWER
# 1.35 s ± 17.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
idx = pd.MultiIndex.from_product([df['Account Number'],
                                 pd.date_range(df['Balance Date'].min(),
                                               df['Balance Date'].max(),
                                               freq='1D')],
                                 names=['Account Number', 'Balance Date'])

df_out= df.set_index(['Account Number', 'Balance Date']).reindex(idx).reset_index()
