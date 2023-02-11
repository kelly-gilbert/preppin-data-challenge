# -*- coding: utf-8 -*-
"""
Preppin' Data 2022: Week 25 - Housing Happy Hotel Guests
https://preppindata.blogspot.com/2022/06/2022-week-25-housing-happy-hotel-guests.html

- Input the data
- Before we bring the 2 datasets together, we want to know how many Additional Requests each guest 
  has made
  - Update N/A values to null and make sure this counts as 0 Additional Requests
- Match the guests to the rooms which have capacity for their entire party
- Filter so that double/twin bed preferences are adhered to
- Ensure guests who have accessibility requirements are only matched with accessible rooms
- Calculate the Request Satisfaction % for each room
- Filter so that guests are only left with rooms with the highest Request Satisfaction %
- Finally, for the rooms with the largest capacity, we want to ensure guests with larger parties are
  prioritised. Filter the data to remove parties that could fit into smaller rooms
- Output the data

Author: Kelly Gilbert
Created: 2023-02-06
Requirements:
  - input dataset:
      - 2022W25 Input.xlsx
  - output dataset (for results check only):
      - 2022W25 Output.csv
"""


from numpy import where
from output_check import output_check    # custom function for checking my output vs. the solution
import pandas as pd


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\2022W25 Input.xlsx') as xl:
    df_room = pd.read_excel(xl, sheet_name='Hotel Rooms')
    df_guest = pd.read_excel(xl, sheet_name='Guests')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# count the number of additional requests
df_guest['Request Count'] = where(df_guest['Additional Requests'].isna(), 
                                  0,
                                  df_guest['Additional Requests'].str.count(',') + 1)


# match based on room capacity, bed size, and accessibility
fill_nas = {'Adults in Party' : 0, 
            'Children in Party' : 0, 
            'Adults' : 0, 
            'Children' : 0}

df_match = ( df_guest.merge(df_room, 
                            how='cross', 
                            suffixes=[' in Party', ''])
                     .fillna(fill_nas)
                     .assign(bed_match = lambda df_x: [1 if bed in features else 0
                                                       for bed, features 
                                                       in zip(df_x['Double/Twin'], df_x['Features'])])
                     .query("`Adults in Party` <= Adults "
                            + " & `Children in Party` <= Children "
                            + " & bed_match == 1"
                            + " & ((`Requires Accessible Room?` == 'Y' "
                            + "     & Features.str.contains('Accessible')) "
                            + "    | `Requires Accessible Room?` != 'Y')") )


# find the % of requests met
df_match['Additional Requests_list'] = ( df_match['Additional Requests'].fillna('')
                                             .str.split(',\s?') )
df_match['Features_list'] = ( df_match['Features'].fillna('')
                                  .str.split(',\s?') )

df_match['Requests Met'] = [sum([1 if r in fl or (r[:3] == 'NOT' and r[4:] not in fl)
                                 else 0 
                                 for r in rl])
                            for rl, fl in zip(df_match['Additional Requests_list'], 
                                              df_match['Features_list'])]   

df_match['Request Satisfaction %'] = where(df_match['Request Count']==0, 
                                           100, 
                                           round(df_match['Requests Met'] 
                                                 / df_match['Request Count'] * 100, 0) )

df_match = ( df_match.loc[df_match['Request Satisfaction %'] 
                          == df_match.groupby('Party')['Request Satisfaction %'].transform('max')] )
 

# keep smallest rooms that will meet the guests' needs
df_match['Capacity_slack'] = where(df_match['Adults'] - df_match['Adults in Party'] > 0,
                                   df_match['Adults'] - df_match['Adults in Party'],
                                   0)

df_match = ( df_match.loc[df_match['Capacity_slack'] 
                          == df_match.groupby('Party')['Capacity_slack'].transform('min')] )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

columns = ['Party', 'Adults in Party', 'Children in Party', 'Double/Twin', 
           'Requires Accessible Room?', 'Additional Requests', 'Request Satisfaction %', 
           'Room', 'Adults', 'Children', 'Features']

( df_match.to_csv(r'.\outputs\output-2022-25.csv', index=False, columns=columns) )


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2022W25 Output.csv']
my_files = [r'.\outputs\output-2022-25.csv']
unique_cols = [['Party', 'Room']]
col_order_matters = True
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)


#---------------------------------------------------------------------------------------------------
# performance comparisons
#---------------------------------------------------------------------------------------------------

# -------- testing separate vs. combined queries ----------

%%timeit
# queries, one step at a time
# 16.7 ms ± 2.81 ms per loop (mean ± std. dev. of 7 runs, 100 loops each) -- SLOWER
df_match = ( df_guest.merge(df_room, 
                            how='cross', 
                            suffixes=['', '_rm'])
                     .fillna(fill_nas)
                     .query("Adults <= Adults_rm & Children <= Children_rm") 
                     .assign(bed_match = lambda df_x: [1 if bed in features else 0
                                                       for bed, features 
                                                       in zip(df_x['Double/Twin'], df_x['Features'])])
                     .query("bed_match == 1")
                     .query("(`Requires Accessible Room?` == 'Y' & Features.str.contains('Accessible')) | `Requires Accessible Room?` != 'Y'") )


%%timeit
# combined queries
# 11.7 ms ± 171 µs per loop (mean ± std. dev. of 7 runs, 100 loops each) -- FASTER
df_match = ( df_guest.merge(df_room, 
                            how='cross', 
                            suffixes=['', '_rm'])
                     .fillna(fill_nas)
                     .assign(bed_match = lambda df_x: [1 if bed in features else 0
                                  for bed, features 
                                  in zip(df_x['Double/Twin'], df_x['Features'])])
                     .query("Adults <= Adults_rm "
                            + " & Children <= Children_rm"
                            + " & bed_match == 1"
                            + " & ((`Requires Accessible Room?` == 'Y' & Features.str.contains('Accessible')) "
                            + "    | `Requires Accessible Room?` != 'Y')") )



# -------- testing different ways to compare the requests vs. room features ----------

%%timeit 
# option 1 - split guest requests into rows, split room features into rows, then join
# 19.1 ms ± 126 µs per loop (mean ± std. dev. of 7 runs, 100 loops each) -- SLOWEST

df_match2 = df_match.copy()
df_match2['Additional Requests'] = df_match2['Additional Requests'].str.split(',\s?')
df_match2['Features'] = ( (df_match2['Features']
                          + where(df_match2['Features'].str.contains('Near to lift'),
                                  '',
                                  ', NOT Near to lift'))
                         .str.split(',\s?') )

df_requests = ( df_match2.explode('Additional Requests')[['Party', 'Room', 'Additional Requests']]
                        .merge(df_match2.explode('Features')[['Party', 'Room', 'Features']],
                               left_on=['Party', 'Room', 'Additional Requests'],
                               right_on = ['Party', 'Room', 'Features'],
                               how='left')
                        .groupby(['Party', 'Room'], as_index=False)
                        .agg(total_requests = ('Additional Requests', 'count'),
                             met_requests = ('Features', 'count'))
                        .assign(Request_Satisfaction_pct = lambda df_x: round(df_x['met_requests'] 
                                                                              / df_x['total_requests']
                                                                              * 100, 0).astype(int)) )

df_match2 = df_match2.merge(df_requests[['Party', 'Room', 'Request_Satisfaction_pct']],
                          on=['Party', 'Room'],
                          how='left')


%%timeit 
# option 2 - split guest requests and compare to room features (as string)
# 1.98 ms ± 145 µs per loop (mean ± std. dev. of 7 runs, 1000 loops each) -- FASTER, however...
#    this could match requests that are a subset and not full match to the request

df_match2 = df_match.copy()
df_match2['Additional Requests'] = df_match2['Additional Requests'].str.split(',\s?')

df_match2['Requests Met'] = [sum([1 if r in fl or (r[:3] == 'NOT' and r[4:] not in fl)
                                 else 0 
                                 for r in rl])
                            for rl, fl in zip(df_match2['Additional Requests'], 
                                              df_match2['Features'])]   
df_match2['Request Satisfaction %'] = round(df_match2['Requests Met'] 
                                           / df_match2['Request Count'] * 100, 0)


%%timeit 
# option 3 - split guest requests into list, split features into list, then compare in list comprehension
# 2.62 ms ± 255 µs per loop (mean ± std. dev. of 7 runs, 100 loops each) -- 2ND PLACE

df_match2 = df_match.copy()
df_match2['Additional Requests'] = df_match2['Additional Requests'].str.split(',\s?')
df_match2['Features'] = df_match2['Features'].str.split(',\s?')
df_match2['Requests Met'] = [sum([1 if r in fl or (r[:3] == 'NOT' and r[4:] not in fl)
                                 else 0 
                                 for r in rl])
                            for rl, fl in zip(df_match2['Additional Requests'], 
                                              df_match2['Features'])]   
df_match2['Request Satisfaction %'] = round(df_match2['Requests Met'] 
                                           / df_match2['Request Count'] * 100, 0)