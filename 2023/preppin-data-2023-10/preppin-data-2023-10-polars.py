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
      - 
"""


from datetime import date, datetime
import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

start_date = date(2023, 1, 31)
end_date = date(2023, 2, 14)


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

# input the csv and keep one record per date 
df = ( pl.scan_csv(r'.\inputs\Account Statements.csv', try_parse_dates=True)
         .sort(by=['Account Number', 'Balance Date', 'Transaction Value'],
               descending=[False, False, True])
         
         # keep one record per account number and date
         .groupby(['Account Number', 'Balance Date'])
         .agg(pl.col('Transaction Value').sum(),
              pl.col('Balance').last())
)


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# generate the list of dates
df_dates = pl.DataFrame(pl.date_range(start_date, end_date, '1d', eager=True)
                          .alias('Balance Date')
                       ).lazy()


# generate all combinations of date/account number and add the actual balance
df_out = ( df.select(pl.col('Account Number').unique())
             .join(df_dates,
                   how='cross')
             .join(df,
                   on=['Account Number', 'Balance Date'],
                   how='left')
             .with_columns(pl.col('Balance').forward_fill())
         )


#---------------------------------------------------------------------------------------------------
# get user input and output the file
#---------------------------------------------------------------------------------------------------

while (user_input := input('Enter the balance date (yyyy-mm-dd format) or Enter to cancel:')) != '':
    try: 
        user_ts = datetime.strptime(user_input, '%Y-%m-%d').date()

    except:
        print(chr(10) + r'Please enter a valid date in yyyy-mm-dd format.', end=chr(10)*2)

    else:
        if user_ts < start_date or user_ts > end_date:
            print(chr(10) + f'Please enter a date between {str(start_date)[0:10]} '\
                  + f'and {str(end_date)[0:10]}.', end=chr(10)*2)
        else:
            filename = fr'.\outputs\Balance as of {str(user_ts)[0:10]}_klg.csv'
            ( df_out
                 .filter(pl.col('Balance Date')==user_ts)
                 .select(pl.col(['Account Number', 'Transaction Value', 'Balance']))
                 .collect()
                 .write_csv(filename)
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
# timing using groupby with maintain_order = True or re-sorting
#---------------------------------------------------------------------------------------------------

# the dataframe needs to be sorted after the groupby to use upsample.

# using the original dataset, both methods were about the same timing, so trying a larger dataset

# make a larger dataset
df = pl.concat([(pl.read_csv(r'.\inputs\Account Statements.csv', try_parse_dates=True)
                   .with_columns(pl.col('Account Number') + 100 + n))
                for n in range (0, 99)])
len(df)    #2M


# method 1: sort after the groupby
# 243 ms ± 8.73 ms per loop (mean ± std. dev. of 7 runs, 1 loop each) -- a little faster
%%timeit
df2 = ( df.sort(by=['Account Number', 'Balance Date', 'Transaction Value'],
               descending=[False, False, True])
         .groupby(['Account Number', 'Balance Date'])
         .agg(pl.col('Transaction Value').sum(),
              pl.col('Balance').last())
         .sort(by=['Account Number', 'Balance Date'],
               descending=False)
         .set_sorted(column=['Account Number', 'Balance Date'],
                     descending=False)
     )


# method 2: groupby with maintain_order
# 291 ms ± 7.11 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
%%timeit 
df2 = ( df.sort(by=['Account Number', 'Balance Date', 'Transaction Value'],
               descending=[False, False, True])
         .groupby(['Account Number', 'Balance Date'], maintain_order=True)
         .agg(pl.col('Transaction Value').sum(),
              pl.col('Balance').last())
         .set_sorted(column=['Account Number', 'Balance Date'],
                     descending=False)
     )


#---------------------------------------------------------------------------------------------------
# timing different methods of filling in the missing dates
#---------------------------------------------------------------------------------------------------

# I explored using upsample to fill in the missing dates, but upsample doesn't fill beyond the 
# existing data. For example, Account Number 73744504 doesn't have a record for Feb 14, so upsample
# would only fill through Feb 13

.upsample(time_column='Balance Date', every='1d', by='Account Number')
.select(pl.all().forward_fill())
