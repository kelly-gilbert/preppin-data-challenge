# -*- coding: utf-8 -*-
"""
Preppin Data Challenge 2020-04
https://preppindata.blogspot.com/2020/01/2020-week-4.html
 
De-duplicating survey data

- Input the data. 
- The first issue is that some people forgot they filled in the survey and 
  filled it out twice with the same information. We need to filter out these 
  duplicates.
- For the first output, we want a count of how many people are watching on each 
  device.
- Unfortunately, this was a free text box on the survey. Many responses have 
  multiple values.
- The Devices Input contains the device types we were hoping for.
- All other answers should be labelled as "Other" - excluding blanks/"etc." 
  responses.
- For the second output, we want to rank each show by its average rating.
- Separate out the shows that respondents have been watching.
- Remove the years in the brackets at the end of each film/show in the UK 
  Netflix content list. Make sure there are no duplicates.
- Join the list of UK Netflix content to the survey responses, so we can check 
  that there hasn't been any confusion (lying) going on when writing a show in 
  the "Other" response free text.
- Only accept "other" responses that have one show in the free text answer, as 
  otherwise we won't know which show the rating refers to!
- Prepare the ratings responses so that we have one column containing all the 
  show names and one containing all the ratings.
- Now combine this with our list of verified shows and the people who watched 
  them.
- Calculate the average rating for each show.
- Create a dense rank so we know what order we should watch these shows in. 
- Output the data

Author: Kelly Gilbert
Created: 2020-08-14
Requirements: input datasets
  - PD 2020W17 Shows and Devices.xlsx
  - PD 2020W17 Survey.xlsx
"""

from os import chdir
from pandas import ExcelFile, read_excel, merge
from numpy import where
import re

chdir('C:\\projects\\preppin-data-challenge\\preppin-data-2020-17')



#------------------------------------------------------------------------------
# import and explore the data
#------------------------------------------------------------------------------

dfSurvey = read_excel(ExcelFile(r'.\inputs\PD 2020W17 Survey.xlsx'))
dfSurvey.head()

inFile = ExcelFile(r'.\inputs\PD 2020W17 Shows and Devices.xlsx')
inFile.sheet_names

dfShows = read_excel(inFile, sheet_name='Netflix Shows')
dfDevices = read_excel(inFile, sheet_name = 'Devices')


# remove completely duplicate rows
#dfSurvey.count()
columnSubset = list(dfSurvey.columns)
columnSubset.remove('Timestamp')
dfSurvey.drop_duplicates(subset=columnSubset, keep='first', inplace=True)
#dfSurvey.count()


# device counts
dfDeviceCount = dfSurvey[['Timestamp', dfSurvey.columns[2]]].copy()
dfDeviceCount.rename(columns={dfSurvey.columns[2] : 'survey_devices'}, inplace=True)
dfDeviceCount['join_field'] = 1
dfDevices['join_field']= 1

dfDeviceCount = merge(dfDeviceCount, dfDevices, how='inner', on='join_field')

dfDeviceCount['flag'] = where(re.match('^|\W' + dfDeviceCount['Device'] + '$|\W', dfDeviceCount['survey_devices']), 1, 0)


dfDeviceCount.columns

- For the second output, we want to rank each show by its average rating.
- Separate out the shows that respondents have been watching.
- Remove the years in the brackets at the end of each film/show in the UK 
  Netflix content list. Make sure there are no duplicates.
- Join the list of UK Netflix content to the survey responses, so we can check 
  that there hasn't been any confusion (lying) going on when writing a show in 
  the "Other" response free text.
- Only accept "other" responses that have one show in the free text answer, as 
  otherwise we won't know which show the rating refers to!
- Prepare the ratings responses so that we have one column containing all the 
  show names and one containing all the ratings.
- Now combine this with our list of verified shows and the people who watched 
  them.
- Calculate the average rating for each show.
- Create a dense rank so we know what order we should watch these shows in. 
- Output the data


