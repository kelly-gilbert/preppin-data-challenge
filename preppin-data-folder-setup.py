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
  - update the main dir below
  - update the new week and week to copy below
  - previous week's .py and folders exist
  
  This will output a shell for the README, but you will need to manually update:
  - The URL for the challenge description
  - Learned/practiced bullets
  
Revisions:
  - Updated README shell to include link to challenge description and practiced/learned bullets
  - Updated README shell to link to .yxzp instead of .yxmd Alteryx files
"""


from os import mkdir, path
from shutil import copy2


# UPDATE VARIABLES HERE:

# main directory path
main_dir = r'C:\myfilepath\Preppin Data Challenge'
new_yr_wk = '2021-20'         # week to add
prev_yr_wk = '2021-21'    # week to copy


# filenames and paths
new_dir = path.join(main_dir, f'{new_yr_wk[:4]}\\preppin-data-{new_yr_wk}')
new_file = f'preppin-data-{new_yr_wk}.py'
prev_dir = path.join(main_dir, f'{prev_yr_wk[:4]}\\preppin-data-{prev_yr_wk}')
prev_file = f'preppin-data-{prev_yr_wk}.py'


# make the main weekly folder and inputs/outputs folders
mkdir(path.join(main_dir, new_dir))
mkdir(path.join(main_dir, new_dir, 'inputs'))
mkdir(path.join(main_dir, new_dir, 'outputs'))


# copy the previous week's script into the main folder as a starter file
copy2(path.join(prev_dir, prev_file), path.join(new_dir, new_file))


# generate the markdown file starter
md = '# Preppin\' Data ' + new_yr_wk[:4] + ' Week ' + str(int(new_yr_wk[-2:])) + chr(10)
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

with open(path.join(new_dir, 'README.md'), 'w') as text_file:
    text_file.write(md)
    