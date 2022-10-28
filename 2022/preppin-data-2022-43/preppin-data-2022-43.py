# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 43 - Missing Training Data 2.0
https://preppindata.blogspot.com/2022/10/2022-week-43-missing-training-data-20.html

- Replace the input data from last week's workflow with the new datasource
- In a new branch, keep only the first training session for each player and each session 
- Work out the minimum date in the entire dataset
- Add in the dates between the minimum date and first session
- Assign these generated dates a Score of 0 and set their flag to be "Pre First Session"
- Combine these new rows with the new rows generated in last weeks challenge
  - Be careful of duplication
- Ensure no weekends exist in your dataset
- Output the data

Author: Kelly Gilbert
Created: 2022-10-26
Requirements:
  - input dataset:
      - Player Training 2.0.csv
  - output dataset (for results check only):
      - 2022W43.csv
"""


from numpy import where
import pandas as pd
#from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df = pd.read_csv(r'.\inputs\Player Training 2.0.csv', parse_dates=['Date'])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# create all combinations of Player, Session, and Date
df_dates = pd.DataFrame({'Date' : pd.date_range(start=df['Date'].min(), 
                                                end=df['Date'].max(), 
                                                freq='1D')})

df_all = ( df[['Player', 'Session']].drop_duplicates()
               .merge(df_dates, how='cross')
               .merge(df, on=['Player', 'Session', 'Date'], how='left')
               .sort_values(by=['Player', 'Session', 'Date']) )


# set the flag
df_all['Flag'] = where(df_all.groupby(['Player', 'Session'])['Score'].ffill().isna(), 
                       'Pre First Session',
                       where(df_all['Score'].isna(), 'Carried over', 'Actual'))


# fill down the score
df_all['Score'] = df_all.groupby(['Player', 'Session'])['Score'].ffill().fillna(0)


# remove weekends
df_all = ( df_all[df_all['Date'].dt.weekday <= 4]
                 .rename(columns={'Date' : 'Session Date'}) )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_all.to_csv(r'.\outputs\output-2022-43.csv', index=False, float_format='%f', date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W43.csv']
my_files = [r'.\outputs\output-2022-43.csv']
unique_cols = [['Player', 'Session', 'Session Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)




#---------------------------------------------------------------------------------------------------
# performance testing different ways to set the flag
#---------------------------------------------------------------------------------------------------

# multiply the original dataset by 200 --> 1.2M records
#df = pd.concat([df.assign(Player=df['Player'] + '-' + str(n)) for n in range(0,200)])




# option 1 - set the flag in multiple steps -- FASTEST

# original dataset = 7.27 ms ± 285 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 3.3M records     = 1.37 s ± 36.3 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
# set the flag (part 1)
df_all['Flag'] = where(df_all['Score'].isna(), 'Carried over', 'Actual')

# fill down the score
df_all['Score'] = df_all.groupby(['Player', 'Session'])['Score'].ffill()

# set the flag (part 2)
df_all['Flag'] = where(df_all['Score'].isna(), 'Pre First Session', df_all['Flag'])

df_all['Score'] = df_all['Score'].fillna(0)




# option 2 - comparison in where (orig vs. fillna) -- a little slower than method 1, similar to method 3

# original dataset = 12.6 ms ± 1.54 ms per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 3.3M records     = 1.87 s ± 22.4 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
# set the flag
df_all['Flag'] = where(df_all.groupby(['Player', 'Session'])['Score'].ffill().isna(), 
                       'Pre First Session',
                       where(df_all['Score'].isna(), 'Carried over', 'Actual'))

# fill down the score
df_all['Score'] = df_all.groupby(['Player', 'Session'])['Score'].ffill().fillna(0)




# option 3 - cumsum to set the flag in one step -- a little slower than method 1, similar to method 2

# original dataset = 14 ms ± 438 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 3.3M records     = 2.42 s ± 44.8 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
# fill down the score
df_all['Score_orig'] = df_all['Score']
df_all['Score'] = df_all.groupby(['Player', 'Session'])['Score'].ffill().fillna(0)


# flag actual vs. carried over from previous session
df_all['Flag'] = where(df_all.groupby(['Player', 'Session'])['Score'].transform('cumsum') == 0, 
                       'Pre First Session',
                       where( df_all['Score_orig'].isna(), 'Carried over', 'Actual'))


df_all.drop(columns=['Score_orig'], inplace=True)



# option 4 - expanding sum to set the flag in one step -- SLOWEST

# original dataset = 14.3 ms ± 149 µs per loop (mean ± std. dev. of 7 runs, 100 loops each)
# 3.3M records     = 3.07 s ± 74.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)

%%timeit 
# reset the index after the sort
df_all.reset_index(drop=True, inplace=True)


# set the flag
df_all['Flag'] = where(df_all.groupby(['Player', 'Session'])['Score'].expanding().min()\
                             .reset_index(drop=True).isna(),
                       'Pre First Session', 
                   where(df_all['Score'].isna(), 'Carried over', 'Actual'))

    
# fill down the score
df_all['Score'] = df_all.groupby(['Player', 'Session'])['Score'].ffill().fillna(0)
