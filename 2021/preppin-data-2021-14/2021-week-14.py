# -*- coding: utf-8 -*-
"""
Preppin' Data 2021: Week 14 - Prep Air In-Flight Purchases
https://preppindata.blogspot.com/2021/04/2021-week-14-prep-air-in-flight.html

- Input the Data
- Assign a label for where each seat is located.
  They are assigned as follows:
  A & F - Window Seats
  B & E - Middle Seats
  C & D - Aisle Seats
- Combine the Seat List and Passenger List tables.
- Parse the Flight Details so that they are in separate fields
- Calculate the time of day for each flight.
  They are assigned as follows:
  Morning - Before 12:00
  Afternoon - Between 12:00 - 18:00
  Evening - After 18:00
- Join the Flight Details & Plane Details to the Passenger & Seat tables. We should be able to
  identify what rows are Business or Economy Class for each flight.
- Answer the following questions:
    - What time of day were the most purchases made? We want to take a look at the average for the
      flights within each time period.
    - What seat position had the highest purchase amount? Is the aisle seat the highest earner
      because it's closest to the trolley?
    - As Business Class purchases are free, how much is this costing us?
    - Bonus: If you have Tableau Prep 2021.1 or later, you can now output to Excel files. Can you
      combine all of the outputs into a single Excel workbook, with a different sheet for each
      output?

Author: Kelly Gilbert
Created: 2021-05-07
Requirements:
  - pandas version 0.25.0 or higher (for explode)
  - input dataset (Week 14 - Input.xlsx)

"""


from numpy import where
from pandas import ExcelFile, ExcelWriter, read_excel


# --------------------------------------------------------------------------------------------------
# input the data
# --------------------------------------------------------------------------------------------------

with ExcelFile(r'.\\inputs\\Week 14 - Input.xlsx') as xl:
    passengers = read_excel(xl, 'Passenger List')
    seats_mtx = read_excel(xl, 'SeatList')
    flight_list = read_excel(xl, 'FlightDetails')
    planes = read_excel(xl, 'PlaneDetails')

# remove extra columns
passengers = passengers[[c for c in passengers.columns if 'Unnamed' not in c]]


# --------------------------------------------------------------------------------------------------
# prep / calculations
# --------------------------------------------------------------------------------------------------

# transpose the seat list
seats = seats_mtx.melt(id_vars='Row', value_vars=seats_mtx.columns[1:])
seats.rename(columns={'variable' : 'Seat Position', 'value' : 'passenger_number'}, inplace=True)

# add the seat type
seat_types = {'A':'Window', 'F':'Window', 'B':'Middle', 'E':'Middle', 'C':'Aisle', 'D':'Aisle'}
seats['Seat Position'] = seats['Seat Position'].map(seat_types)

# parse the flight details
flights = flight_list.iloc[:, 0].str.replace('[\[\]]', '').str.split('|', expand=True)
flights.columns = flight_list.columns[0].replace('[', '').replace(']', '').split('|')
flights['FlightID'] = flights['FlightID'].astype(int)

# calculate the time of day for each flight
flights['Depart Time of Day'] = where(flights['DepTime'] < '12:00:00', 'Morning',
                                  where(flights['DepTime'] <= '18:00:00', 'Afternoon', 'Evening'))

# parse the row types
planes[['min_bc_row', 'max_bc_row']] = planes['Business Class'].str.split('-', expand=True).astype(int)
planes.drop(columns=['Business Class'], inplace=True)

# combine the seat list and passenger list tables
combined = passengers.merge(seats, on='passenger_number', how='left')\
            .merge(flights.merge(planes, left_on='FlightID', right_on='FlightNo.', how='left'),
                   left_on='flight_number', right_on='FlightID', how='left')


# identify the row type (Business Class or Economy)
combined['Business Class'] = where((combined['Row'] >= combined['min_bc_row'])
                                   & (combined['Row'] <= combined['max_bc_row']),
                                   'Business Class', 'Economy')

# checks
len(passengers) == len(combined)    # check for duplication
combined[combined['Business Class'].isna()]        # check for missing row class
combined[combined['Depart Time of Day'].isna()]    # check for missing time of day
combined[combined['Seat Position'].isna()]         # check for missing seat position


# --------------------------------------------------------------------------------------------------
# output the data
# --------------------------------------------------------------------------------------------------

# Q1: what time of day were the most purchases made? (avg spend/flight)
q1 = combined[combined['Business Class'] != 'Business Class']\
              .groupby(['flight_number', 'Depart Time of Day'])['purchase_amount'].sum()\
              .groupby('Depart Time of Day').mean().reset_index()\
              .sort_values(by='purchase_amount', ascending=False)
q1.rename(columns={'purchase_amount' : 'Avg per Flight'}, inplace=True)
q1['Avg per Flight'] = q1['Avg per Flight'].round(2)
q1['Rank'] = q1['Avg per Flight'].rank(ascending=False).astype(int)

# Q2: what seat position had the highest purchase amount? Is the aisle seat the highest earner
#     because it's closest to the trolley?
q2 = combined[combined['Business Class'] != 'Business Class']\
         .groupby('Seat Position')['purchase_amount'].sum().reset_index()\
         .sort_values(by='purchase_amount', ascending=False)
q2.rename(columns={'purchase_amount' : 'Purchase Amount'}, inplace=True)
q2['Rank'] = q2['Purchase Amount'].rank(ascending=False).astype(int)


# Q3: as Business Class purchases are free, how much is this costing us?
q3 = combined.groupby('Business Class')['purchase_amount'].sum().reset_index()\
             .sort_values(by='purchase_amount', ascending=False)
q3.rename(columns={'purchase_amount' : 'Purchase Amount'}, inplace=True)
q3['Rank'] = q3['Purchase Amount'].rank(ascending=False).astype(int)


# write the files to Excel
with ExcelWriter(r'.\outputs\output-2021-14.xlsx') as w:
    q1[['Rank', 'Depart Time of Day', 'Avg per Flight']]\
        .to_excel(w, sheet_name='Time of Day', index=False)
    q2[['Rank', 'Seat Position', 'Purchase Amount']]\
        .to_excel(w, sheet_name='Seat Position', index=False)
    q3[['Rank', 'Business Class', 'Purchase Amount']]\
        .to_excel(w, sheet_name='Business or Economy', index=False)


# --------------------------------------------------------------------------------------------------
# check results
# --------------------------------------------------------------------------------------------------

# checked by visual inspection this week
