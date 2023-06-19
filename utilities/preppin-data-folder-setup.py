# -*- coding: utf-8 -*-
"""
Preppin Data Challenge Folder and Readme Setup

Adds the folder structure for the next challenge week

Directory structure:
preppin-data-challenge
└─ yyyy (year)
   └─ preppin-data-yyyy-mm
      ├─ inputs
      └─ outputs

Author: Kelly Gilbert
Created: 2020-02-18

Requirements:
  - update the variables for MAIN_DIR, NEW_YR_WK (week to be created)
  - Previous Week / Next Weeek navigation in the README does not account for week 53, so you may
    need to manually update the readme at EOY/BOY if there is a week 53
  - templates exist in the _templates folder (.py, .yxmd, and README)
  
  This will output a shell for the README, but you will need to manually update:
  - The URL for the challenge description
  - Learned/practiced bullets
"""


from os import chdir, makedirs, path
from shutil import copy2


# --------------------------------------------------------------------------------------------------
# update variables here
# --------------------------------------------------------------------------------------------------

MAIN_DIR = r'C:\Users\gilbe\projects\preppin-data-challenge'    # main directory path
NEW_YR_WK = '2023-05'    # new week to add


# --------------------------------------------------------------------------------------------------
# calculate previous/future years and weeks
# --------------------------------------------------------------------------------------------------

new_yr = int(NEW_YR_WK[0:4])
new_wk = int(NEW_YR_WK[5:])

last_yr_wk = f'{new_yr if new_wk > 1 else new_yr - 1}-{str(new_wk - 1 if new_wk > 1 else 52).zfill(2)}'
next_yr_wk = f'{new_yr if new_wk < 52 else new_yr + 1}-{str(new_wk + 1 if new_wk < 52 else 1).zfill(2)}'

new_dir = path.join(MAIN_DIR, f'{NEW_YR_WK[:4]}\\preppin-data-{NEW_YR_WK}')


# --------------------------------------------------------------------------------------------------
# folder setup script
# --------------------------------------------------------------------------------------------------

# add the directory structure and templates
if not path.exists(new_dir):
    
    # make subfolders
    makedirs(path.join(MAIN_DIR, new_dir), exist_ok=False)
    makedirs(path.join(MAIN_DIR, new_dir, 'inputs', ), exist_ok=False)
    makedirs(path.join(MAIN_DIR, new_dir, 'outputs'), exist_ok=False)


    # copy the templates into the new directory
    for t in ['alteryx_template.yxmd', 'python_template.py', 'README_template.md']:
        if t == 'README_template.md':
            new_file = 'README.md'
        else:
            new_file = f"preppin-data-{NEW_YR_WK}{t[t.find('.'):]}"
             
        copy2(path.join(MAIN_DIR, f'_templates\{t}'), path.join(new_dir, new_file))
    
    
        # replace the placeholders in the templates
        with open(path.join(new_dir, new_file), 'r') as f:
            f_text = f.read()
            
        f_text = f_text.replace('YYYY', NEW_YR_WK[0:4]).replace('WW', NEW_YR_WK[5:])\
                       .replace('LYLY', last_yr_wk[0:4]).replace('LW', last_yr_wk[5:])\
                       .replace('NYNY', next_yr_wk[0:4]).replace('NW', next_yr_wk[5:])   
                       
        with open(path.join(new_dir, new_file), 'w') as f:
            f.write(f_text)


chdir(new_dir)


import sys
sys.path.append(MAIN_DIR + r'\utilities')
