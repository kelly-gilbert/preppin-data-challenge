# -*- coding: utf-8 -*-
"""
Create a fake dataset modeled after a recruiting workflow history

Created on Fri Nov  4 21:22:09 2022

@author: kelly.gilbert
"""


from numpy import isnan, nan
import pandas as pd
import random as rnd


# --------------------------------------------------------------------------------------------------
# constants
# --------------------------------------------------------------------------------------------------

POSITION_COUNT = 20
CANDIDATE_COUNT = 200
START_DATE = '2021-01-01'
END_DATE = '2022-08-31'


# --------------------------------------------------------------------------------------------------
# functions
# --------------------------------------------------------------------------------------------------

def complete_pos_cand(df):
    return ( df_wf[df_wf['status']=='Offer Accepted']
                  .groupby(['position_id', 'candidate_id'], as_index=False)['status'].size() )


def make_success_stack(position_id, candidate_id):
    start_date = df_pos[df_pos['position_id']==position_id]['start_date'].iloc[0]
    
    df = ( df_status[df_status['mf_flag']==1]
                    .assign(position_id=position_id,
                            candidate_id=candidate_id,
                            start_date=start_date)
                    .reset_index(drop=True) )

    df['ts'] = ( pd.Series([(s + pd.DateOffset(days=(cm + rnd.randint(lb, ub)))
                               + pd.DateOffset(minutes=min(rnd.gammavariate(12*60, 1), 24*60)))
                             for s, cm, lb, ub 
                             in zip(df['start_date'],
                                    df['cuml_max_days'],
                                    df['min_days'], 
                                    df['max_days'])])
                   .astype('datetime64[s]') )
    
    return df


# --------------------------------------------------------------------------------------------------
# create the process step df
# --------------------------------------------------------------------------------------------------

rows = [
    [0, 'Profile Created', nan, 1, 0, 30, 1],  
    
    [1, 'Application Completed', 0, 0.95, 0, 4, 1],
    
    [1.1, 'Candidate Withdrew', 1, 0.025, 0, 5, 0],
    [1.2, 'Application Reviewed', 1, 0.975, 0, 5, 1],

    [2, 'Application Terminated', 1.2, 0.4, 0, 1, 0],
    [2.1, 'Phone Interview Requested', 1.2, 0.6, 0, 1, 1],

    [3, 'Candidate Withdrew', 2.1, 0.03, 0, 3, 0],
    [3.1, 'Phone Interview Scheduled', 2.1, 0.97, 0, 3, 1],

    [4, 'Candidate Withdrew', 3.1, 0.01, 1, 7, 0],    
    [4.1, 'Phone Interview Completed', 3.1, 0.99, 1, 7, 1],
    
    [5, 'Phone Interview Terminated', 4.1, 0.55, 0, 1, 0],
    [5.1, 'On-Site Interview Requested', 4.1, 0.45, 0, 1, 1],

    [6, 'Candidate Withdrew', 5.1, 0.01, 1, 3, 0],    
    [6.1, 'On-Site Interview Scheduled', 5.1, 0.99, 1, 3, 1],
    
    [7, 'Candidate Withdrew', 6.1, 0.1, 14, 20, 0],    
    [7.1, 'On-Site Interview Completed', 6.1, 0.9, 2, 20, 1],
    
    [8, 'On-Site Interview Terminated', 7.1, 0.7, 0, 1, 0],
    [8.1, 'Offer Extended', 7.1, 0.3, 1, 3, 1],

    [9, 'Offer Accepted', 8.1, 0.99, 0, 7, 1],
    [9.1, 'Offer Not Accepted', 8.1, 0.01, 0, 7, 0]
]

df_status = pd.DataFrame(rows, 
                         columns=['status_id', 'status', 'prev_status_id', 'pct_of_prev', 
                                  'min_days', 'max_days', 'mf_flag'])

df_status['step_nbr'] = df_status['status_id'].astype(int)

cumax = df_status.groupby('step_nbr')['max_days'].max().cumsum().shift(1).fillna(0)
df_status['cuml_max_days'] = df_status['step_nbr'].replace(dict(cumax))


# --------------------------------------------------------------------------------------------------
# create the positions and candidates
# --------------------------------------------------------------------------------------------------

# create position and candidate IDs
positions = list(range(1, POSITION_COUNT + 1))
candidates = list(range(1, CANDIDATE_COUNT + 1))


# assign random start dates to positions
date_range = list(pd.date_range(START_DATE, END_DATE, freq='1D'))
df_pos = pd.DataFrame({ 'position_id' : positions,
                        'start_date' : sorted(rnd.choices(date_range, k=POSITION_COUNT)) })


# assign candidates to 1, 2, or 3 positions
df_cp = ( pd.DataFrame({ 'candidate_id' : candidates,
                         'position_id' : [rnd.sample(positions, 
                                                     k=rnd.choices([1, 2, 3], 
                                                                   weights=[0.9, 0.08, 0.02], 
                                                                   k=1)[0])
                                          for i in range(CANDIDATE_COUNT)] })
            .explode('position_id')
            .reset_index(drop=True) )


# --------------------------------------------------------------------------------------------------
# build the workflow history
# --------------------------------------------------------------------------------------------------

df_wf = None
for s in sorted(df_status['prev_status_id'].unique()):

    # if it is the first status, initialize the workflow using all cand/positions
    if isnan(s):
        ids = list(df_status[df_status['prev_status_id'].isna()]['status_id'])
        pcts = list(df_status[df_status['prev_status_id'].isna()]['pct_of_prev'])

        df_add = ( df_cp.merge(df_pos[['position_id', 'start_date']], on='position_id')
                        .rename(columns={'start_date' : 'prev_end'}) )
        
    # otherwise, use the records from the previous status
    else:     
        ids = list(df_status[df_status['prev_status_id']==s]['status_id'])
        pcts = list(df_status[df_status['prev_status_id']==s]['pct_of_prev'])
        df_add = ( df_wf[df_wf['status_id']==s]
                       .drop(columns=['status']) )
        
        prev_end = df_wf.groupby('position_id')['ts'].max().astype('datetime64[D]')
        df_add['prev_end'] = df_add['position_id'].replace(dict(prev_end))


    # assign the next status(es)
    df_add = ( df_add.assign(status_id = list(rnd.choices(ids, weights=pcts, k=len(df_add))))
                     .merge(df_status[['status_id', 'status', 'min_days', 'max_days']], 
                            on='status_id') )

    # assign the status timestamp
    df_add['ts'] = pd.Series([(pe + pd.DateOffset(days=rnd.randint(lb, ub))
                               + pd.DateOffset(minutes=rnd.gammavariate(12*60, 1)))
                              for pe, lb, ub 
                              in zip(df_add['prev_end'], df_add['min_days'], df_add['max_days'])])\
                     .astype('datetime64[s]')
    
    
    # add to the main datset
    df_wf = ( pd.concat([df_wf, 
                         df_add[['candidate_id', 'position_id', 'status_id', 'status', 'ts']]])
                .reset_index(drop=True) )




# --------------------------------------------------------------------------------------------------
# checks
# --------------------------------------------------------------------------------------------------

# ---------- find positions that should have closed (offer accepted), but haven't ----------

total_days = df_status['max_days'].sum()
df_pos['expected_end'] = df_pos['start_date'] + pd.DateOffset(days=total_days)


all_cp = df_wf.groupby(['candidate_id', 'position_id'], as_index=False)['status'].size()

complete_cp = complete_pos_cand(df_wf)

incomplete_p = all_cp[~all_cp['position_id'].isin(complete_cp['position_id'])]['position_id'].unique()


df_add = None
for p in incomplete_p:
    
    # get candidates for the selected position
    incomplete_c = all_cp[all_cp['position_id']==p]['candidate_id'].unique()
                               
    # pick a random incomplete candidate
    c = rnd.choice(incomplete_c)
      
    df_wf = pd.concat([df_wf[(df_wf['candidate_id'] != c) | (df_wf['position_id'] != p)],
                       make_success_stack(p, c)]) 



# ---------- find positions with more than one accepted offer ----------

complete_cp = complete_pos_cand(df_wf)

dup_complete_p = ( complete_cp.groupby('position_id', as_index=False).size()
                       .query('size > 1') )


# pick a random positon to have an offer rejected
rejected = rnd.choice(list(dup_complete_p['position_id']))

for p in [p for p in dup_complete_p['position_id'] if p != rejected]:
    
    # pick the candidates not with the latest offer extended date
    subset = df_wf[(df_wf['position_id']==p) & (df_wf['status']=='Offer Extended')]
    remove_c = list(subset.loc[subset.index != subset['ts'].idxmax()]['candidate_id'])

    # remove the offer accepted status(es)
    df_wf = df_wf[(df_wf['position_id'] != p) | (~df_wf['candidate_id'].isin(remove_c))
                  | (df_wf['status'] != 'Offer Accepted')]
                              
    # replace the offer extended with 'On-Site Interview Terminated'
    mask = df_wf[(df_wf['position_id'] == p) & (df_wf['candidate_id'].isin(remove_c))
                       & (df_wf['status'] == 'Offer Extended')].index
    
    df_wf.loc[mask, 'status'] = 'On-Site Interview Terminated'
    

# handle rejected offer
subset = df_wf[(df_wf['position_id']==rejected) & (df_wf['status']=='Offer Extended')]
reject_c = list(subset.loc[subset.index == subset['ts'].idxmin()]['candidate_id'])

mask = df_wf[(df_wf['position_id'] == rejected) & (df_wf['candidate_id'].isin(reject_c))
                    & (df_wf['status'] == 'Offer Accepted')].index

df_wf.loc[mask, 'status'] = 'Offer Rejected'
df_wf.loc[mask, 'ts'] = subset['ts'].mean()
    


# --------------------------------------------------------------------------------------------------
# build the history file
# --------------------------------------------------------------------------------------------------

# identify the file date for each timestamp
dates = pd.date_range(df_wf['ts'].dt.date.min(), 
                      df_wf['ts'].dt.date.max() + pd.DateOffset(days=1), 
                      freq='1D')
df_dates = pd.DataFrame( { 'file_date' : [d + pd.DateOffset(minutes=3*60 + rnd.randint(0,21)) 
                                          for d in dates]})

df_wf = pd.merge_asof(df_wf.sort_values(by='ts'), df_dates, left_on='ts', right_on='file_date', 
                      direction='forward', allow_exact_matches=True)


# build the file history
df_out = None
for f in df_wf['file_date'].unique():

    # vary the filename formats
    date_fmt = pd.to_datetime(f).strftime('%Y-%m-%d_%H-%M-%S')
    r = rnd.choices([1,2,3], weights=[0.9, 0.1, 0.1], k=1)[0]

    if r==1:
        filename = f"status_history_{date_fmt}.csv"
    elif r==2:
        filename = f"status.history.resend.{date_fmt}.csv"
    else:
        filename = f"workflow-file-{pd.to_datetime(f).strftime('%A')}-{date_fmt}.csv"
    
    # add the history
    # get the unique cand/pos in today's updates, merge with earlier history
    df_add = ( df_wf[df_wf['file_date']==f][['candidate_id', 'position_id']]
                    .drop_duplicates() 
                    .merge(df_wf[df_wf['file_date']<=f], on=['candidate_id', 'position_id'])
                    .drop(columns=['status_id', 'file_date'])
                    .assign(filename=filename) )

    df_out = pd.concat([df_out, df_add])[['candidate_id', 'position_id', 'status', 'ts', 'filename']]


# output the file
df_out.to_csv(r'C:\Users\kelly.gilbert\OneDrive - Chick-fil-A, Inc\Preppin Data Challenge' \
               + '\_challenges\Status History\inputs\status_history_raw.csv',
              index=False, columns=[c for c in df_out.columns if c != 'status_id'])



# --------------------------------------------------------------------------------------------------
# manual checks
# --------------------------------------------------------------------------------------------------

# ---------- candidates with more than one offer extended ----------

dup_offer_c = ( df_wf[df_wf['status']=='Offer Extended']
                     .groupby('candidate_id', as_index=False)['position_id'].size()
                     .query('size > 1') )

if len(dup_offer_c) > 0:
    print('\n\nThe following candidates had offers extended for more than one position:\n')
    print(dup_offer_c)



# ---------- positions with fewer than 2 on-site completed ----------

single_onsite = ( df_wf[df_wf['status']=='On-Site Interview Completed']
                       .groupby('position_id', as_index=False)['candidate_id'].size()
                       .query('size < 2') )

if len(single_onsite) > 0:
    print('\n\nThe following positions had fewer than 2 onsite interviews:\n')
    print(single_onsite)


# ---------- as an example, remove some statuses and replace them  -----------

# pick a candidate who stopped at Phone Interview Terminated
df_last_status = df_wf.loc[df_wf.groupby(['candidate_id', 'position_id'])['ts'].idxmax()]
cands = df_last_status[df_last_status['status']=='Phone Interview Terminated']

change_cands = cands.iloc[rnd.choices(range(0,len(cands)), k=3)][['candidate_id', 'position_id']]
print('\n\nManually modify these candidates:\n')
print(change_cands)

    # pick the next file date
    # copy the last stack
    # replace phone interview terminated with candidate withdrew

# 53 / 8 -- removed phone interview terminated and replaced with candidate withdrew
# 70 / 8 -- removed all phone interview steps and replaced with candidate withdrew
# 114 / 9 --removed phone interview steps and changed app to app terminated




# df_wf[(df_wf['candidate_id']==32) & (df_wf['position_id']==20)][['status', 'ts']]
# subset = df_wf[(df_wf['position_id']==20)][['candidate_id', 'status', 'ts']].sort_values(['candidate_id', 'ts'])

# for c in subset['candidate_id'].unique():
#     print(subset[subset['candidate_id']==c])
#     print('\n\n')

# df_wf[df_wf['candidate_id']==190][['status', 'ts']]

# df_out['filename'].unique()
