# -*- coding: utf-8 -*-
"""
Preppin' Data 2023: Week 52 - Preppin' Classification
https://preppindata.blogspot.com/2023/12/2023-week-52-preppin-classification.html

- Input the data
- Split the themes, so each theme/technique has its own field
- Reshape the data so all the themes are in 1 field
- Group the themes together to account for inaccuracies
  - Don't worry about being too accurate here, the main things to focus on it grouping things like Join/Joins and Aggregate/Aggregation. The way we've chosen to do it leaves us with 73 values, but that did involve a lot of manual grouping.
- Reshape the data so we can see how many challenges each Technique appears in, broken down by Level (as per the output)
- Create a Total field across the levels for each Technique
- Rank the challenges based on the Total field to find out which Techniques we should prioritise for challenge making
- Output the data

Author: Kelly Gilbert
Created: 2024-01-14
Requirements:
  - input dataset:
      - Preppin' Themes.csv
  - output dataset (for results check only):
      - 2023W52 Output.csv
"""


import polars as pl
from output_check import output_check    # custom function for checking my output vs. the solution


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

THEMES_LOOKUP = {
    '% of Total' : 
        ['% of total'],
    'Adding datetime stamp to output' : 
        ['adding datetime stamp to output'],
    'Aggregate' : 
        ['aggregate',
         'aggregates',
         'aggregation',
         'aggrgeate',
         'aggrgegate'],
    'Aggregate Calcs' : 
        ['aggregate calcs'],
    'Aggregate to Deduplicate' : 
        ['aggregate to deduplicate'],
    'Aggregate to correct LOD' : 
        ['aggregate to correct lod'],
    'Append' : 
        ['append',
         'appends'],
    'CASE function' : 
        ['case function'],
    'Changing Data Type at input to avoid nulls' : 
        ['changing data type at input to avoid nulls'],
    'Changing Separator in csv' : 
        ['changing separator in csv'],
    'Clean step only' : 
        ['clean step only'],
    'Cleaning calcs' : 
        ['clean functions',
         'cleaning calcs'],
    'Complex Logical Filters' : 
        ['complex logical filters'],
    'Compound interest' : 
        ['compound interest'],
    'Concatenate' : 
        ['concatenate'],
    'Conversions' : 
        ['conversions'],
    'Country Roles' : 
        ['country roles'],
    'Create Lookup Table' : 
        ['create lookup table'],
    'Currency Conversion' : 
        ['currency conversion'],
    'Custom Fiscal Year' : 
        ['custom fiscal year'],
    'Data Densification' : 
        ['data densification'],
    'Data Interpreter' : 
        ['data interpreter',
         'data interpretor'],
    'Data Roles' : 
        ['data roles'],
    'Date Calcs' : 
        ['convert dates',
         'create date field',
         'date calc',
         'date calcs',
         'date calculation',
         'date calculations',
         'date conversion',
         'date conversions',
         'date functions',
         'date part',
         'date time conversion',
         'make date'],
    'Difference From' : 
        ['% difference from',
         'difference from'],
    'Dynamic Rename' : 
        ['dynamic rename'],
    'Fill down' : 
        ['fill down',
         'fill down 2 fields',
         'filling in blanks'],
    'Filters' : 
        ['filter',
         'filtering',
         'filters',
          'filter duplicates'],
    'Fiscal Date' : 
        ['fiscal date'],
    'Fixed LOD' : 
        ['fixed lod'],
    'Full outer join' : 
        ['full outer join'],
    'Group Values' : 
        ['group values'],
    'Grouping steps' : 
        ['grouping steps'],
    'IF statements' : 
        ['id statment',
         'if statement',
         'if statements',
         'if statments'],
    'Join' : 
        ['join',
         'join practice',
         'simple join'],
    'Left Join' : 
        ['left join',
         'right join'],    # this seems incorrect, but matches the solution
    'Left only join' : 
        ['left only join',
         'right only join'],    # this seems incorrect, but matches the solution
    'Logical Calcs' : 
        ['logical calc',
         'logical calcs'],
    'Lookup' : 
        ['lookup',
         'lookup (but circular)'],
    'Merge fields' : 
        ['merge',
         'merge fields'],
    'Mod function' : 
        ['mod function'],
    'Moving Calculation' : 
        ['moving average',
         'moving calc',
         'moving calculation'],
    'Multiple Join Clause' : 
        ['multi clause join',
         'multiple clause join',
         'multiple join clause',
         'multiptle join clause',
         'mutiple clause join',
         'mutliple join clause',
         'mutliple join clause',
         'mutliptle join clause'],
    'Multiple Pivot' : 
        ['multiple pivot',
         'mutliple pivot'],
    'NPS' : 
        ['nps'],
    'Non Equal Join Clause' : 
        ['<= join clause',
         '>= join clause',
         'non equal join clause',
         'non-equal join clause'],
    'Non inner join' : 
        ['non inner join'],
    'Normalise' : 
        ['normalise'],
    'Numeric Calcs' : 
        ['mathematical calculations',
         'numeric calc',
         'numeric calcs'],
    'Parameter' : 
        ['multiple parameters',
         'parameter',
         'parameter in output name',
         'parameter to name output',
         'parameters',
         'using parameter in output name'],
    'Percentile Rank' : 
        ['percentile rank'],
    'Pivot Cols to Rows' : 
        ['pivot cols',
         'pivot cols to rows'],
    'Pivot Rows to Cols' : 
        ['pivot rows to cols'],
    'Profile Pane' : 
        ['profile pane'],
    'Random' : 
        ['random'],
    'Rank' : 
        ['rank',
         'ranks'],
    'Rank with multiple order bys' : 
        ['rank with multiple order bys'],
    'Regex' : 
        ['regex'],
    'Remove Punctuation' : 
        ['remove punctuation'],
    'Running Total' : 
        ['running sum',
         'running total'],
    'SIGN function' : 
        ['sign function'],
    'Scaffolding' : 
        ['scaffold',
         'scaffolding',
         'scaffolding (through all dimension combinations)'],
    'Self Join' : 
        ['self join'],
    'Source Row Number' : 
        ['source row number'],
    'Space function' : 
        ['space function'],
    'Split' : 
        ['split',
         'splits'],
    'String Calcs' : 
        ['rename values',
         'string calcs',
         'string calculations',
         'string functions'],
    'Targets' : 
        ['targets'],
    'Tile' : 
        ['tile'],
    'Title Case' : 
        ['title case'],
    'Union' : 
        ['union'],
    'Update a workflow' : 
        ['update a workflow',
         'updating a workflow'],
    'Wildcard Union' : 
        ['wildcard union',
         'wildcard input']    # doesn't seem correct, but matches solution
}


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def all_dict_values(d):
    """
    returns a list of all unique values in a dictionary's values
    """
    
    return sorted(list(set([i for v in d.values() for i in v])))


def reverse_explode_dict(d):
    """
    returns a dictionary with the values as keys and the keys as values, 
    with list values exploded into separate keys
    """
    
    return {i:k for k,v in d.items() for i in v}
    
    
#---------------------------------------------------------------------------------------------------
# input and process the data
#---------------------------------------------------------------------------------------------------

df = ( pl.scan_csv(r".\inputs\Preppin' Themes.csv")
      
         # parse the themes and split into rows
         .with_columns(
             pl.col('Themes')
                 .str.to_lowercase()
                 .str.replace_all('joins', 'join')
                 .str.replace_all(r', |/|,$|\s+$', '|')
                 .str.strip_chars('|')
                 .str.split('|')
                 .alias('themes_clean')
         )
         .explode('themes_clean')

         # replace with standard names
         .with_columns( 
             pl.col('themes_clean')
                 .map_dict(reverse_explode_dict(THEMES_LOOKUP),
                           default=pl.col('themes_clean'))
                 .alias('Technique')
         )
         
         # total challenge count for each technique
         .with_columns( 
             pl.col('Technique')
                 .count()
                 .over(pl.col('Technique'))
                 .alias('Total')
         )
    )


# alert on unmapped names
if (missing := [t for t in df.select('themes_clean').unique().collect().to_series() 
                if t not in all_dict_values(THEMES_LOOKUP)]):
    print('*** WARNING: the following themes were not in the lookup:',
          end=chr(10)*2)
    print(f"    {(chr(10) + '    ').join(missing)}",
          end=chr(10)*2)
    

# reshape level into cols
df_out = ( df.collect() 
             .pivot(index=['Total', 'Technique'],
                    columns='Level',
                    values='Year',
                    aggregate_function='count'
             )
             .with_columns(
                 pl.col('Total')
                   .rank(method='dense')
                   .alias('Priority')
             )
         )


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.write_csv(r'.\outputs\output-2023-52.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

solution_files = [r'.\outputs\2023W52 Output.csv']
my_files = [r'.\outputs\output-2023-52.csv']
unique_cols = [['Technique']]
col_order_matters = False
round_dec = 8

output_check(solution_files=solution_files, my_files=my_files, unique_cols=unique_cols, 
             col_order_matters=col_order_matters, round_dec=round_dec)
