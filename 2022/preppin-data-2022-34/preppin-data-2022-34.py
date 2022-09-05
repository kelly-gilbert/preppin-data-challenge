# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 34 - C&BSCo Parameters, Parameters, Parameters
https://preppindata.blogspot.com/2022/08/2022-week-34-c-parameters-parameters.html

- Input data
- Merge Km's and min's as Minutes
- Change 'Value' to Mins
- Split up the unnamed column into:
  - Coach
  - Calories
  - Music Type
- Change Music Type values to be Title Case (first letter of each word is capitalised)
- Create three parameters:
  - Music Type
  - Coach
  - Top N 
- Create a way to return the Top N value selected and order the file with the highest calories burnt at the top
- Create filters so only the parameter selection remains in the output data set
  - For Top N parameter it's all the values up to that number
- Output the data but use the parameter values in the file name so the CEO knows what it contains

Author: Kelly Gilbert
Created: 2022-09-03
Requirements:
  - input dataset:
      - Preppin' Summer 2022 - CEO Cycling.csv
  - output dataset (for results check only):
      - [one example] PD 2022 Wk 34 Output Top 5 for rides with Kym powered by Everything Rock.csv
"""


import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def get_user_input(value_name, value_list):
    """
    present a menu of options to the user and return the user's choice
    """
    
    value_list = sorted(value_list)
    options_str = '\n'.join([f'  {i+1} - {c}' for i,c in enumerate(value_list)])
    
    while True:
        user_input = input(f'\n{value_name.title()} list:\n{options_str}\n\n'
                           + f'Select an option (1 - {len(value_list)}) or press Enter to cancel:')
        
        if user_input.isnumeric() and int(user_input) in range(1, len(value_list)+1):
            return value_list[int(user_input)-1]
        elif user_input == '':
            return user_input
        else:
            print(f'\n*** ERROR: {user_input} is not a valid choice. '
                  + f'Please enter a number between 1 and {len(value_list)}.')


def input_and_prep_data(input_path):
    """
    input and preps the file
    """
    
    # input the data
    df = ( pd.read_csv(input_path, parse_dates=['Date'], dayfirst=True)
             .rename(columns={'Value' : 'Mins'})
             .rename(columns=lambda c: 'Unnamed' if 'Unnamed' in c else c)
         )


    # split the unnamed column and change music type to title case
    df[['Coach', 'Calories', 'Music Type']] = df['Unnamed'].str.extract('(.*)\s+-\s+(\d+)\s+-\s+(.*)')
    df['Music Type'] = df['Music Type'].str.strip().str.title()
    df['Calories'] = df['Calories'].astype(int)
    
    return df[['Coach', 'Calories', 'Music Type', 'Date', 'Mins']]


def output_file(df, coach, music_type, n):
    """
    filter the data and output the file
    """
    
    # top in by calories burned
    df_out = df.loc[(df['Coach'] == coach) 
                    & (df['Music Type'] == music_type), df.columns]
    
    # rank by calories burned
    df_out['Rank'] = df_out.groupby(['Coach', 'Music Type'])['Calories'].rank(ascending=False, 
                                                                              method='dense')
    
    
    # output the file
    filepath = f'.\\outputs\\output-2022-34 - Top {n} for rides with {coach} powered by {music_type}.csv'
    ( df_out[df_out['Rank'] <= n]
          .sort_values('Rank', ascending=True)
          .to_csv(filepath, index=False, date_format='%d/%m/%Y')
    )
    
    print(f"\n*** File created: {filepath}")


#---------------------------------------------------------------------------------------------------
# main loop - get user input and output the file
#---------------------------------------------------------------------------------------------------

df = input_and_prep_data(r".\inputs\Preppin' Summer 2022 - CEO Cycling.csv")


while True:    
    coach = get_user_input('Coach', df['Coach'].unique())
    if coach == '':
        break
        
    music_type = get_user_input('Music type', df['Music Type'].unique())
    if music_type == '':
        break
    
    n = input('\nReturn the top n sessions by calories burned (or press Enter to cancel):\n')
    if n == '':
        break
    elif not n.isnumeric() or int(n) <= 0:
        print(f'\n*** ERROR: {n} is not a valid number. Please enter a number greater than zero.')
        break
    
    output_file(df, coach, music_type, int(n))


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r".\outputs\PD 2022 Wk 34 Output Top 5 for rides with Kym powered by Everything Rock.csv"]
my_files = [r'.\outputs\output-2022-34 - Top 5 for rides with Kym powered by Everything Rock.csv']
unique_cols = [['Coach', 'Music Type', 'Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
