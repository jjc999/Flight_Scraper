from Flights import Flights
from GoogleFlights import GoogleFlights
from ExpediaFlights import ExpediaFlights
from FlightParser import FlightParser

# 1 = Test Flights Class, 2 = Test Flight Parser Class, 3 = Test Expedia Flights Class
test_class = 2

# Test Flights Class
# ###################
# my_flight = Flights()
# my_flight.set_end_airport('Copenhagen')
# print('Flight from ')
# my_flight.get_start_airport(0)
# print(' to ')
# my_flight.get_end_airport(0)
#
# my_flight.get_flight_info()
#
# new_info = ['OAK', 'CPH', 'May 20', 'May 25', 500, 8, 'One-Way']
# my_flight.set_flight_info(new_info)
# my_flight.get_flight_info()

# Test Flight Parser Class
# #########################
if test_class == 2:
    flight = FlightParser()
    search_engine = GoogleFlights(flight.browser)
    flight.select_flight_searcher(search_engine=search_engine)
    flight.user_flight_info()
    flight.search()

# Test Expedia Flights Class
# ###########################
if test_class == 3:
    print('')
    flight2 = ExpediaFlights()
    # flight2.get_flight_info()

    flight2.user_flight_info()
    # flight2.scrape_prices(url)

# Test Google Flights Class
# print('')
# flight2 = GoogleFlights()
# flight2.get_flight_info()
#
# flight2.user_flight_info()

# TODO:
# Write google flights class that has methods that extract data from google flights.  Then I can have a method
# called something like 'get_flight_info()' for each class built for different flight websites (like Norwegian or
# something) and call that in a loop to easily gather all of the flight info
