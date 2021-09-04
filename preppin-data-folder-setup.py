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
  - update the variables for main_dir, new_yr_wk (week to be created), and prev_yr_wk (week to copy)
  - Previous Week / Next Weeek navigation in the README does not account for week 53, so you may
    need to manually update the readme at EOY/BOY if there is a week 53
  - main folder and .py file exists for the specified previous week
  - Alteryx shell file exists in main preppin-data-challenge folder
  
  This will output a shell for the README, but you will need to manually update:
  - The URL for the challenge description
  - Learned/practiced bullets
  
Revisions:
  - Updated README shell to include link to challenge description and practiced/learned bullets
  - Updated README shell to link to .yxzp instead of .yxmd Alteryx files
  - Added Alteryx file shell
"""


# --------------------------------------------------------------------------------------------------
# UPDATE VARIABLES HERE:
# --------------------------------------------------------------------------------------------------

main_dir = r'C:\projects\preppin-data-challenge'    # main directory path
new_yr_wk = '2021-34'     # new week to add
prev_yr_wk = '2021-32'    # week to copy


# --------------------------------------------------------------------------------------------------
# folder setup script
# --------------------------------------------------------------------------------------------------

from os import mkdir, path
from shutil import copy2


# filenames and paths
new_dir = path.join(main_dir, f'{new_yr_wk[:4]}\\preppin-data-{new_yr_wk}')
new_file = f'preppin-data-{new_yr_wk}.py'
prev_dir = path.join(main_dir, f'{prev_yr_wk[:4]}\\preppin-data-{prev_yr_wk}')
prev_file = f'preppin-data-{prev_yr_wk}.py'


# make the main weekly folder and inputs/outputs folders
mkdir(path.join(main_dir, new_dir))
mkdir(path.join(main_dir, new_dir, 'inputs'))
mkdir(path.join(main_dir, new_dir, 'outputs'))


# copy the previous week's .py file into the new week's folder as a starter file
copy2(path.join(prev_dir, prev_file), path.join(new_dir, new_file))


# copy the Alteryx workflow template into the new week's folder as a starter file
copy2(path.join(main_dir, 'alteryx_template.yxmd'), path.join(new_dir, f'preppin-data-{new_yr_wk}.yxmd'))


# generate the markdown file starter
new_wk_nbr = int(new_yr_wk[-2:])
week_ago_wk_nbr = new_wk_nbr-1 if new_wk_nbr > 1 else 52
week_ago_yr_wk = f'{(int(new_yr_wk[0:4]) - (0 if new_wk_nbr > 1 else 1))}-{("0"+str(week_ago_wk_nbr))[-2:]}'
next_wk_nbr = new_wk_nbr+1 if new_wk_nbr < 52 else 1
next_yr_wk = f'{(int(new_yr_wk[0:4]) + (0 if new_wk_nbr < 52 else 1))}-{("0" + str(next_wk_nbr))[-2:]}'

md = f'<h6><a href="..\preppin-data-{week_ago_yr_wk}\README.md">◀  Prev Week</a>&nbsp;&nbsp;&nbsp;'\
    + f'|&nbsp;&nbsp;&nbsp;<a href="..\preppin-data-{next_yr_wk}\README.md">Next Week  ▶</a></h6>'
md += chr(10)
md += chr(10)
md += '# Preppin\' Data ' + new_yr_wk[:4] + ' Week ' + str(int(new_yr_wk[-2:])) + chr(10)
md += chr(10)

md += '[Challenge description](https://preppindata.blogspot.com/2021/)' + chr(10) + chr(10)

md += 'What I learned/practiced this week:' + chr(10)
md += '*' + chr(10)
md += '*' + chr(10)
md += '*' + chr(10)
md += chr(10)

md += '## Python' + chr(10)
md += f'<a href="preppin-data-' + new_yr_wk + '.py">' + chr(10)
md += '<img src="img-python-code-' + new_yr_wk + '.png?raw=true" alt="Python code">' + chr(10)
md += '</a>' + chr(10)
md += chr(10)

md += '## Alteryx' + chr(10)
md += '<a href="preppin-data-' + new_yr_wk + '.yxzp">' + chr(10)
md += '<img src="img-alteryx-' + new_yr_wk + '.png?raw=true" alt="Alteryx workflow">' + chr(10)
md += '</a>'

with open(path.join(new_dir, 'README.md'), 'w', encoding='utf-8') as text_file:
    text_file.write(md)
    
