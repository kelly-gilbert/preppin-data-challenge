# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 12 - Graduate Student Loan Repayments (polars)
https://preppindata.blogspot.com/2024/03/2024-week-12-graduate-student-loan.html

- Input the data
- In the Undergraduate Loans table, create a row for every year of the course   
  - This will represent the payment date for each year (it should fall on 1st September)
- Calculate the number of months between the payment date and April 2024
- Join with the Repayment details table
- Calculate the Amount Borrowed + the Interest applied
  - Compound interest will be useful here 
- Total these values together so only 1 row remains and graduates can clearly see the total amount they borrowed and where it stands now that interest has been applied
- Introduce a Salary parameter with values of potential graduate salaries:
  - £30,000
  - £35,000
  - £40,000
- Workout what their monthly repayment will be, based on the above information
- Also work out how much interest will be applied in the following month, after the repayment is made 
- Output the data

Author: Kelly Gilbert
Created: 2024-03-24
Requirements:
  - input dataset:
      - 2024W12 Input.xlsx
  - output dataset (for results check only):
      - N/A - checked by visual inspection
"""


import polars as pl


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

CURRENT_DATE = '2024-04-01'
SALARY = 35_000
INPUT_PATH = r'.\inputs\2024W12 Input.xlsx'


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def month_diff(date1, date2):
    """calculate the number of months between date 1 and date 2"""
    
    return ( (date2.dt.year() - date1.dt.year()) * 12 \
             + (date2.dt.month() - date1.dt.month()) \
             + pl.when((date2.dt.day() >= date1.dt.day()) 
                       | (date2 == date2.dt.month_end()))
                   .then(0)
                   .otherwise(-1)
           )          
             
   
#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

df_loans = pl.DataFrame()
for k, v in pl.read_excel(INPUT_PATH, sheet_id=0).items():
    if k=='Repayment':
        df_repay = v
    else:
        df_loans = pl.concat([df_loans, 
                              v.with_columns(
                                  pl.lit(k)
                                    .str.replace(' Loans', '')
                                    .alias('Loan'))])


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

df = ( df_loans
           # convert course start to date
           .with_columns(
               ('1 ' + pl.col('Course Start'))
                   .str.to_date(format='%d %B %Y')
                   .alias('Course Start'),
               pl.col('Course Length (years)')
                   .add(-1)
                   .cast(pl.String())
                   .add('y')
                   .alias('Offset') 
           )
           
           # generate one row per year
           .with_columns(
               pl.date_ranges(
                   pl.col('Course Start'), 
                   pl.col('Course Start').dt.offset_by(pl.col('Offset')),
                   interval='1y')
                   .alias('Payment Date'),
              pl.lit(CURRENT_DATE).str.to_date().alias('Current Date')
           )
           .explode('Payment Date')
           
           # join to the repayment table
           .join( 
               df_repay,
               on='Loan',
               how='left'
               )
           
           # calculate annual principal + interest
           .with_columns(
               month_diff(pl.col('Payment Date'),
                          pl.col('Current Date'))
                   .alias('Month Count')
           )
           .with_columns(
               ( pl.col('Amount per year') * (1 + pl.col('Interest')/12) ** pl.col('Month Count') )
                   .alias('Total Borrowed + Interest')
           )       
    )


# summary
df_out = ( df
              .select(
                   pl.col('Amount per year').sum().alias('Total Borrowed'),
                   pl.col('Total Borrowed + Interest').sum().round(2),
                   pl.col('Repayment Threshold').first(),
                   pl.col('% Repayment over Threshold').first(),
                   pl.col('Interest').first()
              )
              .with_columns(
                   ((SALARY - pl.col('Repayment Threshold')) \
                       * pl.col('% Repayment over Threshold')/100/12)
                        .round(2)
                        .alias('Monthly Repayment')
              )
              .with_columns( 
                  (pl.col('Total Borrowed + Interest') - pl.col('Monthly Repayment'))
                      .alias('Total Borrowed + Interest')
              )
              .with_columns(
                  (pl.col('Total Borrowed + Interest') * pl.col('Interest')/12)
                      .round(2)
                      .alias('Interest to be added next month')
              )
              .select(pl.all()
                          .exclude([
                              'Repayment Threshold', 
                              '% Repayment over Threshold', 
                              'Interest']
                           )
              )
         )

    
#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.write_csv(r'.\outputs\output-2024-12.csv')


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection
