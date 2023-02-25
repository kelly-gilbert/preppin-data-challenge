# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 46 - Dynamically Fixing Table Structures
https://preppindata.blogspot.com/2022/11/2022-week-46-dynamically-fixing-table.html

- Input the data
- Bring in the data from all the Regions and update the workflow so that no rows get duplicated
- Output the data

Author: Kelly Gilbert
Created: 2022-11-30
Requirements:
  - input dataset:
      - Strange table structure updated.xlsx
  - output dataset (for results check only):
      - Week 46 Output.csv
"""


from numpy import nan, where
import pandas as pd
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------



#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------
 



# option 1: process each file separately (do week 45, but iterate for each file)
%%timeit 
in_path = r'.\inputs\Strange table structure updated.xlsx'


def readsheet(in_path, s):
    with pd.ExcelFile(in_path) as xl:
        year = pd.read_excel(xl, sheet_name=s, header=None, nrows=1, usecols=[0]).iloc[0, 0][-4:]
        df = pd.read_excel(xl, sheet_name=s, skiprows=1, header=[1,2])
    
    # melt the columns into rows, then pivot metrics into cols
    df_p = ( df.melt(id_vars=[df.columns[0]])
               .set_axis(['Store', 'Month', 'Metric', 'value'], axis=1)
               .pivot_table(values='value', 
                            index=['Store', 'Month'], 
                            columns='Metric', 
                            aggfunc='sum')
                          .reset_index() 
               .assign(Region=s))

    df_p['Date'] = pd.to_datetime(df_p['Month'] + ' ' + str(year))
    
    return df_p
    

df = pd.concat([readsheet(in_path, s) for s in pd.ExcelFile(in_path).sheet_names])


# output
( df.drop(columns='Month')
      .to_csv(r'.\outputs\output-2022-46.csv', index=False, date_format='%d/%m/%Y') )









# option 2: bring in all records, with no col names. Melt data and then join back to get the col month/metric
%%timeit
with pd.ExcelFile(r'.\inputs\Strange table structure updated.xlsx') as xl:
    df = ( pd.concat([pd.read_excel(xl, sheet_name=s, header=None)\
                        .assign(Region=s)
                      for s in xl.sheet_names])
             .reset_index(drop=True) )


# fill in the year
df['year'] = pd.Series(where(df[0].str[:5] == 'Table', df[0].str[-4:], nan)).ffill()


# extract the column names
cols = df.iloc[2:4].T.ffill()
dict(cols[2])


# melt the columns into rows, then pivot metrics into cols
df_p = ( df.loc[~df[1].isna() & ~df[2].isna() & (df[0] != 'Store')]
           .melt(id_vars=['Region', 'year', df.columns[0]], var_name='col_name'))
           
df_p['Month'] = pd.to_datetime(df_p['col_name'].replace(dict(cols[2])) + ' ' + df_p['year'])           
           
           
           .set_axis(['Region', 'year', 'Store', 'col_num', 'value'], axis=1)
           .pivot_table(values='value', 
                        index=['Store', 'col_num'], 
                        columns='Metric', 
                        aggfunc='sum')
                      .reset_index() )

df_p['Date'] = pd.to_datetime(df_p['Month'] + ' ' + str(year))






# option 3: 
    
    
# cases to handle:
# store name starts with "Table"
# sheets have different numbers of months
# sheets have different years


# fill in the year
df['year'] = pd.Series(where(df[0].str[:5] == 'Table', df[0].str[-4:], nan)).ffill()


# extract the column names
cols = df.iloc[2:4].T.ffill()
cols
dict(cols[2])


# melt the columns into rows, then pivot metrics into cols
df_p = ( df.loc[~df[1].isna() & ~df[2].isna() & (df[0] != 'Store')]
           .melt(id_vars=['Region', 'year', df.columns[0]], var_name='col_name'))
           
df_p['Month'] = pd.to_datetime(df_p['col_name'].replace(dict(cols[2])) + ' ' + df_p['year'])           
           
           
           .set_axis(['Region', 'year', 'Store', 'col_num', 'value'], axis=1)
           .pivot_table(values='value', 
                        index=['Store', 'col_num'], 
                        columns='Metric', 
                        aggfunc='sum')
                      .reset_index() )

df_p['Date'] = pd.to_datetime(df_p['Month'] + ' ' + str(year))



#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

( df.drop(columns='Month')
      .to_csv(r'.\outputs\output-2022-46.csv', index=False, date_format='%d/%m/%Y') )











#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\Week 46 Output.csv']
my_files = [r'.\outputs\output-2022-46.csv']
unique_cols = [['Store', 'Region', 'Date']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
