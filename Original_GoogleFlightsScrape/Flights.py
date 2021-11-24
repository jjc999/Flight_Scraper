class Flights:
    # Default Constructor
    def __init__(self):
        self.start_airport = 'SLC'
        self.end_airport = 'Rome'
        self.date_leave = 'Jul 31'
        self.date_leave_orig = self.date_leave
        self.date_leave_final = self.date_leave
        self.date_return = 'Aug 3'
        self.date_return_orig = self.date_return
        self.price = 1200
        self.duration = 10
        self.flight_type = 'Round Trip'
        self.date_list = []
        self.price_list = []
        self.date_mat = []
        self.dates_length_list = []
        self.dates_length_mat = []
        self.price_mat = []
        self.month_list = []
        self.year_price_mat = [[] for x in range(0, 12)]
        self.flight_ind = 0
        self.num_flights = 1

    # Getters
    def get_start_airport(self, nargout):
        if nargout == 1:
            return self.start_airport
        else:
            print(self.start_airport)

    def get_end_airport(self, nargout):
        if nargout == 1:
            return self.end_airport
        else:
            print(self.end_airport)

    def get_date_leave(self, nargout):
        if nargout == 1:
            return self.date_leave
        else:
            print(self.date_leave)

    def get_date_return(self, nargout):
        if nargout == 1:
            return self.date_return
        else:
            print(self.date_return)

    def get_price(self, nargout):
        if nargout == 1:
            return str(self.price)
        else:
            print(self.price)

    def get_duration(self, nargout):
        if nargout == 1:
            return str(self.duration)
        else:
            print(self.duration)

    def get_flight_type(self, nargout):
        if nargout == 1:
            return self.flight_type
        else:
            print(self.flight_type)

    def get_flight_info(self):
        print('--------------------------------------')
        print('Flight from ' + self.get_start_airport(1) + ' to ' + self.get_end_airport(1) +
              ' (' + self.get_flight_type(1) + ')')
        print('--------------------------------------')
        print('Departure: ' + self.get_date_leave(1))
        print('Return: ' + self.get_date_return(1))
        print('Price: $' + self.get_price(1))
        print('Duration: ' + self.get_duration(1) + ' hrs')

    # Setters
    def set_start_airport(self, new_start_airport):
        self.start_airport = new_start_airport

    def set_end_airport(self, new_end_airport):
        self.end_airport = new_end_airport

    def set_date_leave(self, new_date_leave):
        self.date_leave = new_date_leave

    def set_date_return(self, new_date_return):
        self.date_return = new_date_return

    def set_price(self, new_price):
        self.price = new_price

    def set_duration(self, new_duration):
        self.duration = new_duration

    def set_flight_type(self, new_flight_type):
        self.flight_type = new_flight_type

    def set_flight_info(self, new_flight_info):
        # Unpack flight info (new_flight_info is list
        new_start_airport = new_flight_info[0]
        new_end_airport = new_flight_info[1]
        new_date_leave = new_flight_info[2]
        new_date_return = new_flight_info[3]
        new_price = new_flight_info[4]
        new_duration = new_flight_info[5]
        new_flight_type = new_flight_info[6]

        # Store flight info in object
        self.set_start_airport(new_start_airport)
        self.set_end_airport(new_end_airport)
        self.set_date_leave(new_date_leave)
        self.set_date_return(new_date_return)
        self.set_price(new_price)
        self.set_duration(new_duration)
        self.set_flight_type(new_flight_type)
