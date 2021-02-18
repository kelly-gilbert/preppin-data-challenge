# -*- coding: utf-8 -*-
"""
Preppin Data Challenge Setup

Adds the folder structure for the next challenge week

Directory structure:
preppin-data-challenge
└─ preppin-data-yyyy-mm
   ├─ inputs
   └─ outputs

Author: Kelly Gilbert
Created: 2020-02-18

Requirements:
  - previous week's .py and folders exist
  - main directory and current year/week variables manually updated below
"""


from os import chdir, mkdir
from shutil import copy2


# update the year/week to add and enter your main directory path
year = 2021
week = 7    # week to add
prev_year = 2021
prev_week = 6
main_dir = 'C:\\projects\\preppin-data-challenge\\'

chdir(main_dir)
yr_wk = str(year) + '-' + ('0' + str(week))[-2:]
prev_yr_wk = str(prev_year) + '-' + ('0' + str(prev_week))[-2:]


# create the weekly folder and inputs/outputs folders
new_dir = '.\\' + str(year) + '\\preppin-data-' + yr_wk
new_file = 'preppin-data-' + yr_wk + '.py'

mkdir(new_dir)
mkdir(new_dir + '\\inputs')
mkdir(new_dir + '\\outputs')


# copy the previous week's script into the main folder as a starter file
prev_dir = '.\\' + str(year) + '\\preppin-data-' + prev_yr_wk
prev_file = 'preppin-data-' + prev_yr_wk + '.py'
    
copy2(prev_dir + '\\' + prev_file, new_dir + '\\' + new_file)


# generate the markdown file starter
md = '# Preppin\' Data ' + str(year) + ' Week ' + str(week) + chr(10)
md += chr(10)

md += '## Python' + chr(10)
md += '<a href="preppin-data-' + yr_wk + '.py">' + chr(10)
md += '<img src="img-python-code-' + yr_wk + '.png?raw=true" alt="Python code">' + chr(10)
md += '</a>' + chr(10)
md += chr(10)

md += '## Alteryx' + chr(10)
md += '<a href="/preppin-data-' + yr_wk + '.yxmd">' + chr(10)
md += '<img src="img-alteryx-' + yr_wk + '.png?raw=true" alt="Alteryx workflow">' + chr(10)
md += '</a>'

with open(new_dir + "\\README.md", "w") as text_file:
    text_file.write(md)