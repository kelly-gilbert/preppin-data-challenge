# -*- coding: utf-8 -*-
"""
Created on Sat Apr  9 21:35:55 2022

@author: kelly.gilbert
"""

import pandas as pd


def output_check(solution_files, my_files, unique_cols, col_order_matters = False, round_dec = 8):
    """
    Checks the solution_files against my_files and outputs any differences.

    Parameters
    ----------
    solution_files : LIST
        A list of file paths for the solution files.
    my_files : LIST
        A list of file paths for my files. Files must be in the same order as solution_fies.
    unique_cols : LIST
        A list of lists of fields to join on.
    col_order_matters : BOOLEAN, optional
        Does the order of columns need to match the solution? The default is False.
    round_dec : TYPE, optional
        The number of decimal places to compare. The default is 8.

    Returns
    -------
    None.

    """
    
   
    for i, solution_file in enumerate(solution_files):
        print('---------- Checking \'' + solution_file + '\' ----------\n')
    
        # read in the files
        df_sol = pd.read_csv(solution_file)
        df_mine = pd.read_csv(my_files[i])
    
        # are the columns the same?
        solution_cols = list(df_sol.columns)
        myCols = list(df_mine.columns)
        if not col_order_matters:
             solution_cols.sort()
             myCols.sort()
    
        col_match = False
        if solution_cols != myCols:
            print('*** Columns do not match ***')
            print('    Columns in solution: ' + str(list(df_sol.columns)))
            print('    Columns in mine    : ' + str(list(df_mine.columns)))
            print('\n\n')
        else:
            print('Columns match\n')
            col_match = True
    
    
        # are the values the same? (only check if the columns matched)
        if col_match:
            errors = 0
            df_compare = df_sol.merge(df_mine, how='outer', on=unique_cols[i],
                                      suffixes=['_sol', '_mine'], indicator=True)
            
            # extra/missing records
            if len(df_compare[df_compare['_merge'] != 'both']) > 0:
                print('\n\n*** Missing or extra records ***')
                print('\n\nIn solution, not in mine:\n')
                print(df_compare[df_compare['_merge'] == 'left_only'][unique_cols[i]])
                print('\n\nIn mine, not in solution:\n')
                print(df_compare[df_compare['_merge'] == 'right_only'][unique_cols[i]]) 
                errors += 1
    
            # for the records that matched, check for mismatched values
            for c in [c for c in df_sol.columns if c not in unique_cols[i]]:
                if 'float' in df_compare[f'{c}_sol'].dtype.name:
                    df_compare[f'{c}_sol'] = df_compare[f'{c}_sol'].round(round_dec)
                    df_compare[f'{c}_mine'] = df_compare[f'{c}_mine'].astype(float).round(round_dec)
                    
                unmatched = df_compare[(df_compare['_merge']=='both')
                                       & (df_compare[f'{c}_sol'] != df_compare[f'{c}_mine'])
                                       & ((df_compare[f'{c}_sol'].notna()) 
                                          | (df_compare[f'{c}_mine'].notna()))]
    
                if len(unmatched) > 0:
                    print(f'\n\n*** Values do not match: {c} ***\n')
                    print(unmatched[unique_cols[i] + [f'{c}_sol', f'{c}_mine']])
                    print('\n')
                    errors += 1
            
            if errors == 0:
                print('Values match')
    
        print('\n')  
