class userData:
  def __init__(self):
    # Set default values for data members
    self.departure_airport = 'SLC'
    self.arrival_airport = 'Rome'
    self.date_leave = 'Jul 31'
    self.date_return = 'Aug 3'
    self.flight_type = 'Round Trip'  # round trip vs. one-way

    # Ask user for flight info
    self.set_user_data()

  def set_user_data(self):
    # Ask the user to input the flight information they want to search
    print('///////////////////////////////')
    print('Enter in Desired Flight Info')
    print('///////////////////////////////')
    self.departure_airport = input('From: ')
    self.arrival_airport = input('To: ')
    self.flight_type = input('Flight Type (Round Trip/One-Way): ')
    self.date_leave = input('Departing on (MM/DD/YY): ')
    if self.flight_type == 'Round Trip':
        self.date_return = input('Returning on (MM/DD/YY): ')
    else:
        self.date_return = ""

  def get_user_data(self):
    print('/////////////////')
    print('User Search Data')
    print('/////////////////')
    print('From : ' + self.departure_airport)
    print('To: ' + self.arrival_airport)
    print('Flight Type: ' + self.flight_type)
    print('Departing on ' + self.date_leave)
    print('Returning on ' + self.date_return)