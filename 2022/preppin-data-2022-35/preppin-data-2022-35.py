# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 35 - C&BSCo Summary Stats
https://preppindata.blogspot.com/2022/08/2022-week-35-c-summary-stats.html

- Input data
- Merge km's and min's as Minutes
- Split the unnamed column into
  - Coach
  - Calories
  - Music Type
- Convert the Dates to Years
- Create a parameter to let the user select any speed as the average riding speed (KPH)
  - Your values may differ depending on my average speed (I used 30 kph)
- Create the following aggregations
  - Total Minutes
  - Total Minutes per Coach (find the most minutes per Coach)
  - Calories per Minute per Coach (find the max calories per minute per Coach)
  - Avg. Calories per Ride
  - Total Rides
  - Total Distance ((Mins/60)*Speed Parameter)
  - Avg. Calories per Minute 
- Combine all the answers and restructure your data if necessary
- Output the data

Author: Kelly Gilbert
Created: 2022-09-05
Requirements:
  - input dataset:
      - Preppin' Summer 2022 - CEO Cycling.csv
  - output dataset (for results check only):
      - [example w/ 30 kph] PD 2022 Wk 35 Output.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# define functions
#---------------------------------------------------------------------------------------------------

def to_float(in_str):
    """
    if in_str is a float, return the float value. otherwise, return None
    """
    
    try:
        return float(in_str)
    except:
        return None


def input_and_prep(kph):
    """
    input the file and perform initial data prep
    """
    
    # input and prep data
    df =  ( pd.read_csv(r".\inputs\Preppin' Summer 2022 - CEO Cycling.csv", 
                        parse_dates=['Date'], dayfirst=True)
              .rename(columns={'Value' : 'Mins'})
              .rename(columns=lambda c: 'Unnamed' if 'Unnamed' in c else c)
              .drop(columns=['Units', 'Type'])
          )

    df[['Coach', 'Calories', 'Music Type']] = df['Unnamed'].str.extract('(.*)\s+-\s+(\d+)\s+-\s+(.*)')
    df['Music Type'] = df['Music Type'].str.strip().str.title()
    df['Year'] = -df['Date'].dt.year
    df['Calories'] = df['Calories'].astype(int)
    df['Distance'] = kph * df['Mins'] / 60
    
    return df


def aggregate_and_output(df):
    """
    perform aggregations and generate the output file
    """
    
    # aggregate by year
    df_agg = ( df.groupby(['Year'])
                 .agg(Total_Mins=('Mins', 'sum'),
                      Total_Calories=('Calories', 'sum'),
                      Total_Rides=('Mins', 'count'),
                      Total_Distance=('Distance', 'sum'))
             )
    df_agg['Avg. Calories per Ride'] = (df_agg['Total_Calories'] / df_agg['Total_Rides']).round(1)
    df_agg['Avg. Calories per Minute'] = (df_agg['Total_Calories'] / df_agg['Total_Mins']).round(1)


    # aggregate by year and coach
    df_coach = ( df.groupby(['Year', 'Coach'], as_index=False)
                   .agg(Mins=('Mins', 'sum'),
                        Calories=('Calories', 'sum'))
               )
    
    df_coach['Calories per Min'] = df_coach['Calories'] / df_coach['Mins']
    df_coach['Calories per Minute per Coach'] = ( df_coach['Coach'] + ' (' 
                                       + (df_coach['Calories per Min']).round(1).astype(str) + ')' )
    df_coach['Total Mins per Coach'] = df_coach['Coach'] + ' (' + df_coach['Mins'].astype(str) + ')'


    # add the coach aggregations to the total df
    df_all = ( pd.concat([df_agg.drop(columns=['Total_Calories']), 
                          df_coach.iloc[df_coach.groupby('Year')['Mins'].idxmax()]
                                                .set_index('Year')
                                                ['Total Mins per Coach'],
                          df_coach.iloc[df_coach.groupby('Year')['Calories per Min'].idxmax()]
                                                .set_index('Year')
                                                ['Calories per Minute per Coach']],
                          axis=1)
                .rename(columns=lambda c: c.replace('_', ' '))
             )    
    
 
    # reshape the df so measures are in rows and years are in cols, then output the data  
    ( df_all.melt(ignore_index=False, var_name='Measure')
            .pivot_table(index='Measure', values='value', columns='Year', aggfunc='first')
            .reset_index()
            .rename(columns=lambda c: str(c).replace('-', ''))
            .to_csv(r'.\outputs\output-2022-35.csv', index=False)
    )
    
    print('*** File output complete.')


#---------------------------------------------------------------------------------------------------
# get user input for speed and generate the file
#---------------------------------------------------------------------------------------------------

while True:
    input_kph = input('Enter the average pace (kph):')
    kph = to_float(input_kph)
    
    if input_kph == '' :
        break
    elif kph == None or kph <= 0:
        print(f'*** ERROR: {input_kph} is not a vailid number. Please enter a number > 0.')
    else:
        df = input_and_prep(kph)
        aggregate_and_output(df)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\PD 2022 Wk 35 Output.csv']
my_files = [r'.\outputs\output-2022-35.csv']
unique_cols = [['Measure']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
