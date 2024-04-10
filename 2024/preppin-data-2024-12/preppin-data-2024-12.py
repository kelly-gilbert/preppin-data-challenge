# -*- coding: utf-8 -*-
"""
Preppin' Data 2024: Week 12 - Graduate Student Loan Repayments
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


from numpy import where
import pandas as pd
from pandas.tseries.offsets import MonthEnd


#---------------------------------------------------------------------------------------------------
# constants
#---------------------------------------------------------------------------------------------------

CURRENT_DATE = '2024-04-01'
SALARY = 35_000


#---------------------------------------------------------------------------------------------------
# functions
#---------------------------------------------------------------------------------------------------

def month_diff(date1, date2):
    """calculate the number of months between date 1 and date 2"""

    return (date2.dt.year - date1.dt.year) * 12 + (date2.dt.month - date1.dt.month) \
             + where((date2.dt.day >= date1.dt.day) 
                     | (date2 == date2 + MonthEnd(0)),
                    0,
                    -1)
                     

#---------------------------------------------------------------------------------------------------
# input the data
#---------------------------------------------------------------------------------------------------

with pd.ExcelFile(r'.\inputs\2024W12 Input.xlsx') as xl:
    df_loans = ( pd.read_excel(xl, 0)
                   .assign(Loan = xl.sheet_names[0].replace(' Loans', '')) )
    df_repay = pd.read_excel(xl, sheet_name='Repayment')


#---------------------------------------------------------------------------------------------------
# process the data
#---------------------------------------------------------------------------------------------------

# payment date and number of months since; join with repayment table
df = ( df_loans
           # create one row per year of course
           .assign(Course_Start_Date = pd.to_datetime(df_loans['Course Start'], format='%B %Y'))
           .assign(Year = lambda df_x: [range(1, cl+1) for cl in df_x['Course Length (years)']])
           .explode('Year')
           .assign(Payment_Date = \
                       lambda df_x: [csd + pd.offsets.DateOffset(years=y-1)
                                     for csd, y in zip(df_x['Course_Start_Date'],
                                                       df_x['Year'])],
                   Current_Date = pd.to_datetime(CURRENT_DATE))
           .assign(Month_Count = \
                       lambda df_x: month_diff(df_x['Payment_Date'], 
                                               df_x['Current_Date']))
          .merge(df_repay,
                 on='Loan',
                 how='inner')
           )

df['Principal_plus_Interest'] = df['Amount per year'] * (1 + df['Interest']/12) ** df['Month_Count']


# summary
df_out = ( df[['Amount per year', 'Principal_plus_Interest']]
               .sum()
               .round(2)
               .to_frame()
               .T
               .rename(columns={'Amount per year' : 'Total Borrowed',
                                'Principal_plus_Interest' : 'Total Borrowed + Interest'})
         )

df_out['Monthly Repayment'] = ((SALARY - df.iloc[0]['Repayment Threshold']) \
                                  * df.iloc[0]['% Repayment over Threshold'] / 100 / 12).round(2)

df_out['Total Borrowed + Interest'] -= df_out['Monthly Repayment']     
df_out['Interest to be added next month'] = \
    (df_out['Total Borrowed + Interest'] * df.iloc[0]['Interest']/12).round(2)


#---------------------------------------------------------------------------------------------------
# output the file
#---------------------------------------------------------------------------------------------------

df_out.to_csv(r'.\outputs\output-2024-12.csv', index=False)


#---------------------------------------------------------------------------------------------------
# check results
#---------------------------------------------------------------------------------------------------

# checked by visual inspection
