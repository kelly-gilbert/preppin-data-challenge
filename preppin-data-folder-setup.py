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

# update the year/week to add and enter your main directory path
year = 2020
week = 12    # week to add
prev_week = 3
prev_year = 2020
main_dir = 'C:\\projects\\preppin-data-challenge'



from os import chdir, mkdir
from shutil import copy2


chdir(main_dir)

# create the weekly folder and inputs/outputs folders
new_dir = '.\\preppin-data-' + str(year) + '-' + ('0' + str(week))[-2:]
new_file = 'preppin-data-' + str(year) + '-' + ('0' + str(week))[-2:] + '.py'

mkdir(new_dir)
mkdir(new_dir + '\\inputs')
mkdir(new_dir + '\\outputs')


# copy the previous week's script into the main folder as a starter
prev_dir = '.\\preppin-data-' + str(prev_year) + '-' + ('0' + str(prev_week))[-2:]
prev_file = 'preppin-data-' + str(prev_year) + '-' + ('0' + str(prev_week))[-2:] + '.py'
    
copy2(prev_dir + '\\' + prev_file, new_dir + '\\' + new_file)


# change the working directory to the new week's folder
chdir(new_dir)