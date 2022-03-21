# -*- coding: utf-8 -*-

"""
Update the Preppin' Data README

- Combine the completed challenge lists for all years
- Parse the Preppin' Data Challenge Index from the blog and add the challenge title 
- Combine the Alteryx and Python tool/function indexes for all years

Author: Kelly Gilbert
Created: 2022-03-19

Requirements:
- None

"""


from numpy import where
import pandas as pd
import requests
from bs4 import BeautifulSoup


list_url = 'https://preppindata.blogspot.com/p/the-challenge-index.html'


# --------------------------------------------------------------------------------------------------
# parse the challenge list on the Preppin' Data blog
# --------------------------------------------------------------------------------------------------

# get the challenge list page, replace br with div
# (some sections have a separate div per challenge, some are separated by brs)
r = requests.get(list_url)
soup = BeautifulSoup(r.text.replace('<br />','</div><div>'), "lxml")


# find the main body of the post, skip the next 2 divs, find all remaining divs
post_body = soup.find(id="post-body-8969973131645153856")\
                .nextSibling.nextSibling.nextSibling
divs = post_body.find_all('div')


# for each div, extract the text and the challenge link
out_list = []
for d in divs:
    t = d.text
    links = [a.get('href') for a in d.find_all('a') if 'Challenge' in a.text]
    link = links[0] if len(links) > 0 else None
    out_list.append([t, link])


# convert to a DataFrame and parse columns
df_pd = pd.DataFrame(out_list, columns=['text', 'challenge_url'])\
       .assign(text=lambda df_pd_x: df_pd_x['text'].str.strip())

# fill down the year
df_pd['year'] = pd.Series(where(df_pd['text'].str.match('\d+'), df_pd['text'], None)).str.strip()\
               .ffill()

# parse the week # and title
pattern = 'Week (\d+):\s*(?:Challenge\s+|Solution\s+|Video\s+)+(.*)'
df_pd[['week', 'title']] = df_pd['text'].str.extract(pattern)

df_pd = df_pd.loc[df_pd['challenge_url'].notna()].drop(columns='text')


# write out to csv
df_pd.to_csv(r'C:\users\gilbe\projects\preppin-data-challenge\challenge_list.csv')


# matches expected count?
print(len(df_pd) == 46 + 53 + 52 + 10)


# --------------------------------------------------------------------------------------------------
# get the yearly tables from github
# --------------------------------------------------------------------------------------------------

# currently, the weeks completed and alteryx/python indexes are in separate READMEs for each year
# these will be combined into a single index in the main README


# import the existing tables from the year summaries on github
df_mine = pd.DataFrame()
df_alteryx = pd.DataFrame()
df_python = pd.DataFrame()

for y in range(2019, 2023):
    year_url = f'https://github.com/kelly-gilbert/preppin-data-challenge/tree/master/{y}#readme'
    tables = pd.read_html(year_url)

    df_mine = pd.concat([df_mine, tables[0].assign(year=str(y))])
    df_alteryx = pd.concat([df_alteryx, tables[1].assign(year=str(y))])
    df_python = pd.concat([df_python, tables[2].assign(year=str(y))])


# melt the weeks into individual rows
df_mine = df_mine.melt(id_vars='year', var_name='col', value_name='week')\
                 .assign(week=lambda df_x: df_x['week'].str.replace('Week ', ''))\
                 .drop(columns='col')\
                 .dropna()

df_alteryx[['Category', 'Tool']] = df_alteryx[['Category', 'Tool']].ffill()
df_alteryx = df_alteryx.assign(Challenges = df_alteryx['Challenges'].str.split())\
                       .explode('Challenges')\
                       .dropna()

df_python['Category'] = df_python['Category'].ffill()
df_python = df_python.assign(Challenges=df_python['Challenges'].str.split())\
                     .explode('Challenges')\
                     .dropna()


# --------------------------------------------------------------------------------------------------
# create the combined challenge list (with links to challenges I have completed)
# --------------------------------------------------------------------------------------------------

# join the list of challenges and weeks completed
df_all = df_pd.merge(df_mine, on=['year', 'week'], how='outer', indicator=True)


# check for mismatches (should only happen if I have completed a week that is not in the official list yet)
print('\nChallenge weeks in mine, but not in the official challenge list:\n')
print(df_all[df_all['_merge'] == 'right_only'])


# output table markdown
df_all['table_line'] = \
    '|' + df_all['week'] + '|' + df_all['title'] + '|[📝](' + df_all['challenge_url'] + ')|' \
    + where(df_all['_merge'] == 'left_only', '|',  
            '[✅](' + df_all['year'] + '/preppin-data-' + df_all['year'] + '-' \
                + df_all['week'].str.zfill(2) + '/README.md)|')

spacer = df_all['title'].str.len().max() * 1.6 - len('Challenge')
table_md = '|Week|Challenge' + '&nbsp;' * int(spacer) + '|Challenge<br>Description|My Solutions|\n' + \
           '|-:|:----------|:-:|:-:|\n' + \
           '\n'.join(df_all['table_line'].astype(str))

print(table_md)


# --------------------------------------------------------------------------------------------------
# create the combined Alteryx index
# --------------------------------------------------------------------------------------------------

# HTML table for easier maintenance
df_alteryx = df_alteryx.sort_values(by=['Category', 'Tool', 'year', 'Challenges'])  

df_alteryx['week_link'] = '      <a href="' + df_alteryx['year'] + '/preppin-data-' + df_alteryx['year'] \
                              + '-' + df_alteryx['Challenges'].str.replace('W','') + '/README.md">' \
                              + df_alteryx['Challenges'] + '</a>&nbsp;&nbsp;&nbsp;'


# group by year
df_alteryx_g = df_alteryx.groupby(['Category', 'Tool', 'year'], as_index=False)\
                         .agg(links=('week_link', lambda x: x.str.cat(sep='\n')))
df_alteryx_g['links'] = '\n      <b>' + df_alteryx_g['year'] + ':</b>&nbsp;' \
                            + df_alteryx_g['year'].str.replace('[^1]', '', regex=True)\
                                                  .str.replace('1', '&nbsp;', regex=False) \
                            + '\n' + df_alteryx_g['links']


# group by tool
df_alteryx_g = df_alteryx_g.groupby(['Category', 'Tool'], as_index=False)\
                           .agg(links=('links', lambda x: x.str.cat(sep='')))


# output the table markdown
df_alteryx_g['Category'] = where(df_alteryx_g['Category'] != df_alteryx_g['Category'].shift(1),
                                 df_alteryx_g['Category'], '')

df_alteryx_g['table_line'] = '  <tr>\n    <td>\n      ' + df_alteryx_g['Category'] \
                                 + '\n    </td>\n    <td>\n      ' + df_alteryx_g['Tool'] \
                                 + '\n    </td>\n    <td>      ' + df_alteryx_g['links'] \
                                 + '\n    </td>\n  </tr>\n'
                                 
df_alteryx_g['table_line'] = df_alteryx_g['table_line'].str.replace('<td>\s+<\/td>', '<td></td>', regex=True)

table_md = '<table>\n  <tr>\n    <td><b>Category</b></td>\n    <td><b>Tool</b></td>\n' \
               + '    <td><b>Weeks Used</b></td>\n  </tr>\n\n' + \
               '\n'.join(df_alteryx_g['table_line'].astype(str)) + \
               '</table>'

with open('alteryx_table_html.txt', 'w') as out_file:
        out_file.write(table_md)
        

# --------------------------------------------------------------------------------------------------
# create the combined Python index
# --------------------------------------------------------------------------------------------------

# HTML table for easier maintenance
df_python = df_python.sort_values(by=['Category', 'Function/Method/Concept', 'year', 'Challenges'])  

df_python['week_link'] = '      <a href="' + df_python['year'] + '/preppin-data-' + df_python['year'] \
                              + '-' + df_python['Challenges'].str.replace('W','') + '/README.md">' \
                              + df_python['Challenges'] + '</a>&nbsp;&nbsp;&nbsp;'


# group by year
df_python_g = df_python.groupby(['Category', 'Function/Method/Concept', 'year'], as_index=False)\
                       .agg(links=('week_link', lambda x: x.str.cat(sep='\n')))
df_python_g['links'] = '\n      <b>' + df_python_g['year'] + ':</b>&nbsp;' \
                            + df_python_g['year'].str.replace('[^1]', '', regex=True)\
                                                  .str.replace('1', '&nbsp;', regex=False) \
                            + '\n' + df_python_g['links']


# group by tool
df_python_g = df_python_g.groupby(['Category', 'Function/Method/Concept'], as_index=False)\
                           .agg(links=('links', lambda x: x.str.cat(sep='')))


# output the table markdown
df_python_g['Category'] = where(df_python_g['Category'] != df_python_g['Category'].shift(1),
                                 df_python_g['Category'], '')

df_python_g['table_line'] = '  <tr>\n    <td>\n      ' + df_python_g['Category'] \
                                 + '\n    </td>\n    <td>\n' \
                                 + '\n```' + df_python_g['Function/Method/Concept'] \
                                 + '```\n    </td>\n    <td>\n      ' + df_python_g['links'] \
                                 + '\n    </td>\n  </tr>\n'

df_python_g['table_line'] = df_python_g['table_line'].str.replace('<td>\s+<\/td>', '<td></td>', regex=True)

table_md = '<table>\n  <tr>\n    <td><b>Category</b></td>\n    <td><b>Function/Method/Concept</b></td>\n' \
               + '    <td><b>Weeks Used</b></td>\n  </tr>\n\n' + \
               '\n'.join(df_python_g['table_line'].astype(str)) + \
               '</table>'

with open('python_table_html.txt', 'w') as out_file:
        out_file.write(table_md)
