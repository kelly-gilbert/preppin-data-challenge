# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 34 - Excelling with lookups
https://preppindata.blogspot.com/2021/08/2021-week-34-excelling-with-lookups.html

- Input data
- Calculate the Average Monthly Sales for each employee
- In the Targets sheet the Store Name needs cleaning up
- Filter the data so that only employees who are below 90% of their target on average remain
- For these employees, we also want to know the % of months that they met/exceeded their target
- Output the data

Author: Kelly Gilbert
Created: 2021-08-25
Requirements:
  - input dataset:
      - 2021 Week 34 Input.xlsx
"""


from numpy import where
from pandas import ExcelFile, melt, merge, read_excel


def stack_dict(in_dict):
    """
    stack all of the name options as keys, with the correct spelling as value
    """
    
    new_dict = { i:k for k, v in in_dict.items() for i in v}    
    new_dict.update({ k:k for k in in_dict.keys() })
    return new_dict


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

store_map = { 'Bristol' : ['Bristal', 'Bristole', 'Bristoll'],
              'Stratford' : ['Statford' , 'Stratfod', 'Straford', 'Stratfodd'],
              'Wimbledon' : ['Wimbledan', 'Vimbledon', 'Wimbledone'],
              'York' : ['Yor', 'Yorkk', 'Yark']
            }


with ExcelFile(r'.\inputs\2021 Week 34 Input.xlsx') as xl:
    sales = read_excel(xl, 'Employee Sales')\
            .melt(id_vars=['Store', 'Employee'], var_name='Month', value_name='Sales')
    targets = df = read_excel(xl, 'Employee Targets')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# clean store name in targets
store_map_stack = stack_dict(store_map)
targets['Store'] = targets['Store'].replace(store_map_stack)

missing_stores = [s for s in targets['Store'].unique() if s not in store_map_stack.keys()]
if len(missing_stores) > 0:
    print('The following stores names are not present in the lookup:\n' + '\n'.join(missing_stores))


# join sales to targets
sales = sales.merge(targets, on=['Store', 'Employee'], how='left')
sales['met_target_flag'] = where(sales['Sales'] >= sales['Monthly Target'], 1, 0)


# summarize
summary = sales.groupby(['Store', 'Employee']).agg(Avg_monthly_Sales=('Sales', 'mean'),
                                                   pct_of_months_target_met=('met_target_flag', 'mean'),
                                                   Monthly_Target=('Monthly Target', 'mean'))\
                                              .reset_index()
summary.columns = [c.replace('pct_', '%_').replace('_', ' ') for c in summary.columns]


# keep employees below 90% of target
summary = summary.loc[summary['Avg monthly Sales'] < summary['Monthly Target'] * 0.9]


# % of months meeting target
summary['% of months target met'] = round(summary['% of months target met'] * 100, 0)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

out_cols = ['Store', 'Employee', 'Avg monthly Sales', '% of months target met', 'Monthly Target']
summary.to_csv(r'.\outputs\output-2021-34.csv', index=False, columns=out_cols)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection this week