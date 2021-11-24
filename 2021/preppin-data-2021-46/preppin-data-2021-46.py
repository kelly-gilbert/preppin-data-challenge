# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 46 Book Shop Data Modelling
https://preppindata.blogspot.com/2021/11/2021-week-46-book-shop-data-modelling.html

- Input data
- Union all the Sales data together to form one row per item in a sale
    - This is the granularity of the data set throughout the whole challenge (56,350 rows)
- Join all other data sets in the workbook on to this data
    - Never let the number of rows change
    - You may need to disregard incomplete records or summarise useful data into a metric instead of including all the detail
- Remove any duplicate fields
- Remove the two fields created (in Prep at least) as the result of the Union:
    - Table Names
    - Sheet Names
- Output your resulting single table

Author: Kelly Gilbert
Created: 2021-11-23
Requirements:
  - input dataset:
      - Bookshop.xlsx
  - output dataset (for results check only):
      - PD 2021 Wk 46 Output.csv
"""


from pandas import concat, DataFrame, ExcelFile, merge, read_excel

# for results check only
from pandas import read_csv


#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Bookshop.xlsx') as xl:
    # read the dimension sheets into a dictionary of DataFrames
    d = {}
    for s in [s for s in xl.sheet_names if 'Sales' not in s]:
        d[s] = read_excel(xl, s)

    # read the sales sheets into a single DataFrame
    df_sales = concat([read_excel(xl, s).assign(sheet_name=s) 
                       for s in xl.sheet_names if 'Sales' in s])


#---------------------------------------------------------------------------------------------------
# exploring the data
#---------------------------------------------------------------------------------------------------

# make a combined list of all of the columns in each dataframe
df_cols = concat([DataFrame({'col_name' : d[s].columns}).assign(df_name=s) for s in d.keys()])


# take all of the cols from the output, and figure out the source of each col and join fields

# 'Book ID', 'Format', 'PubID', 'Publication Date', 'Pages', 'Print Run Size (k)', 'Price' 
#    --> Edition (join to sales on ISBN)
# 'Sale Date', 'ISBN', 'Discount', 'ItemID', 'OrderID' --> sales
# 'Title', 'AuthID' --> Book (join using Book ID from Edition)
# 'First Name', 'Last Name', 'Birthday', 'Country of Residence', 'Hrs Writing per Day' 
#    --> Author (join on AuthID from Book)
# 'Publishing House', 'City', 'State', 'Country', 'Year Established', 'Marketing Spend' 
#    --> Publisher (join on PubID from Edition)
# 'Number of Awards Won (avg only)' --> Award (aggregate on title from Book, then join on title)
# 'Number of Months Checked Out', 'Total Checkouts'--> checkouts (join on BookID from Edition)
# 'Genre', 'SeriesID', 'Volume Number', 'Staff Comment'
#      --> Info (append BookID 1 and 2 and then join that to Book ID from Book)
# 'Series Name', 'Planned Volumes', 'Book Tour Events' --> Series (join to SeriesID from Info)
# 'Average Rating', 'Number of Reviewers', 'Number of Reviews' --> Ratings (summarize by BookID)


# ISBN from Edition is unique?
d['Edition']['ISBN'].count() == d['Edition']['ISBN'].nunique()

# BookID from Book is unique?
d['Book']['BookID'].count() == d['Book']['BookID'].nunique()

# AuthID from Author is unique?
d['Author']['AuthID'].count() == d['Author']['AuthID'].nunique()

# PubID from Publisher is unique?
d['Publisher']['PubID'].count() == d['Publisher']['PubID'].nunique()

# BookID from Info is unique?
(d['Info']['BookID1'] + d['Info']['BookID2'].astype(str)).count() == \
    (d['Info']['BookID1'] + d['Info']['BookID2'].astype(str)).nunique()
    
# SeriesID from Series is unique?
d['Series']['SeriesID'].count() == d['Series']['SeriesID'].nunique()


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# join all other data sets in the workbook on to this data
# - Never let the number of rows change
# - You may need to disregard incomplete records or summarise useful data into a metric instead of 
#   including all the detail

df = df_sales.merge(d['Edition'], on='ISBN', how='left')\
             .merge(d['Book'], on='BookID', how='left')\
             .merge(d['Author'], on='AuthID', how='left')\
             .merge(d['Publisher'], on='PubID', how='left')\
             .merge(d['Award'].groupby('Title')['Year Won'].size().reset_index()\
                              .rename(columns={'Year Won' : 'Number of Awards Won (avg only)'}),
                    on='Title', how='left')\
             .merge(d['Checkouts'].groupby('BookID')\
                                  .agg(Number_of_Months_Checked_Out=('CheckoutMonth', 'nunique'),
                                       Total_Checkouts=('Number of Checkouts', 'sum')).reset_index(),
                    on='BookID', how='left')\
             .merge(d['Info'].assign(BookID=d['Info']['BookID1'] + d['Info']['BookID2'].astype(str),
                                     Staff_Comment=d['Info']['Staff Comment'].str.strip()),
                    on='BookID', how='left')\
             .merge(d['Series'], on='SeriesID', how='left')\
             .merge(d['Ratings'].groupby('BookID').agg(Average_Rating=('Rating', 'mean'),
                                                       Number_of_Reviewers=('ReviewerID', 'nunique'),
                                                       Number_of_Reviews=('ReviewID', 'count')),
                    on='BookID', how='left')\
             .drop(columns=['sheet_name', 'BookID1', 'BookID2', 'Staff Comment'])\
             .rename(columns={'BookID' : 'Book ID'})

             
# remove underscores from col names
df.columns = [c.replace('_', ' ') for c in df.columns]


# check record count
print(f'Number of records after merge: {len(df)}')


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df.to_csv(r'.\outputs\output-2021-46.csv', index=False, date_format='%d/%m/%Y')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = ['PD 2021 Wk 46 Output.csv']
my_files = ['output-2021-46.csv']
col_order_matters = False

for i, solution_file in enumerate(solution_files):
    print('---------- Checking \'' + solution_file + '\' ----------\n')

    # read in the files
    df_solution = read_csv('.\\outputs\\' + solution_file)
    df_mine = read_csv('.\\outputs\\' + my_files[i])

    # are the fields the same and in the same order?
    solution_cols = list(df_solution.columns)
    myCols = list(df_mine.columns)
    if not col_order_matters:
         solution_cols.sort()
         myCols.sort()

    col_match = False
    if solution_cols != myCols:
        print('*** Columns do not match ***')
        print('    Columns in solution: ' + str(list(df_solution.columns)))
        print('    Columns in mine    : ' + str(list(df_mine.columns)))
    else:
        print('Columns match\n')
        col_match = True

    # are the values the same? (only check if the columns matched)
    if col_match:
        # round float values
        s = df_solution.dtypes.astype(str)
        for c in s[s.str.contains('float')].index:
            df_solution[c] = df_solution[c].round(6)
            df_mine[c] = df_mine[c].round(6)

        # join the dataframes on all columns except the in flags
        df_solution_compare = df_solution.merge(df_mine, how='outer',
                                                on=list(df_solution.columns),
                                                suffixes=['_solution', '_mine'], indicator=True)

        if len(df_solution_compare[df_solution_compare['_merge'] != 'both']) > 0:
            print('*** Values do not match ***\n')
            print('In solution, not in mine:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'left_only']) 
            print('\n\n')
            print('In mine, not in solution:\n')
            print(df_solution_compare[df_solution_compare['_merge'] == 'right_only']) 
            
        else:
            print('Values match')

    print('\n')
