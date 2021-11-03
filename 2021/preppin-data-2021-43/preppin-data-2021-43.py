# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 43 - Is that the case?
https://preppindata.blogspot.com/2021/10/2021-week-43-is-that-case.html

- Input the data
- From the Business Unit A Input, create a Date Lodged field
- Use the lookup table to update the risk rating
- Bring Business Unit A & B together
- We want to classify each case in relation to the beginning of the quarter (01/10/21):
    - Opening cases = if the case was lodged before the beginning of the quarter   
    - New cases = if the case was lodged after the beginning of the quarter
- In order to count cases closed/deferred within the quarter, we want to call out cases with a 
  completed or deferred status
- For each rating, we then want to count how many cases are within the above 4 classifications
- We then want to create a field for Cases which will carry over into the next quarter
    - i.e. Opening Cases + New Cases - Completed Cases - Deferred Cases
- Reshape the data to match the final output
- Output the data

Author: Kelly Gilbert
Created: 2021-10-27
Requirements:
  - input dataset:
      - 2021W43 Input.xlsx
  - output dataset (for results check only):
      - no output dataset this week (visually inspected vs. the screen shot)
"""


from numpy import where
from pandas import concat, ExcelFile, pivot_table, read_excel
from pandas import read_csv    # for answer check only


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\inputs\2021W43 Input.xlsx') as xl:
    df_risk = read_excel(xl, 'Risk Level')
    df_a = read_excel(xl, 'Business Unit A ', parse_dates={'Date lodged' : ['Month ', 'Date', 'Year']})
    df_b = read_excel(xl, 'Business Unit B ', skiprows=5, parse_dates=['Date lodged'], dayfirst=True)\
           .rename(columns={'Unit' : 'Business Unit '})


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# use the lookup table to update the risk rating for business unit A
risk_dict = dict(zip(df_risk['Risk level'], df_risk['Risk rating']))
df_a['Rating'] = df_a['Rating'].replace(risk_dict)


# bring Business Unit A & B together
df = concat([df_a, df_b])
df.columns = [c.strip() for c in df.columns]


# classify each case in relation to the beginning of the quarter
df['Quarter Status'] = where(df['Date lodged'] < '2021-10-01', 'Opening cases', 'New cases')


# melt the two status columns into rows, then pivot into columns
df_p = df.melt(id_vars=['Ticket ID', 'Rating'], value_vars=['Status', 'Quarter Status'],
               value_name='Status')\
         .pivot_table(values='Ticket ID', index='Rating', columns=['Status'], aggfunc='size',
                      fill_value=0)\
         .drop(columns=['In Progress'])\
         .reset_index()


# calculte the cases continuing
df_p['Continuing'] = df_p['Opening cases'] + df_p['New cases'] - df_p['Completed'] - df_p['Deferred']


# un-pivot for final output
df_out = df_p.melt(id_vars=['Rating'], var_name='Status', value_name='Cases')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2021-43.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week
solution_df = read_csv(r'.\outputs\output-2021-32.csv')
print(solution_df.sort_values(['Rating', 'Status']))
