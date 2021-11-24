from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import requests
from bs4 import BeautifulSoup
import time
import datetime


class GoogleFlights:
    def __init__(self, browser):
        # Store browser input (Selenium)
        self.browser = browser

        # Get action chain
        self.actions = ActionChains(self.browser)

        # Initialize list that will store input box elements
        self.input_boxes = []

    def search(self, user_info):
        # Method to actually search google flights based on user inputs
        # ---------------------------------------------------------------

        # Select Flight Type, Input Dates, and starting and ending airports
        self.select_flight_type(user_info)

        # Search for each combination of starting and ending airports the user input
        # TODO: Need to update call to scrape_calendar (and method itself) to handle multiple airport searches
        #  This includes plotting the correct data, storing the data for each airport combination correctly,
        #  resetting the dates for each search, and plotting all the curves on the same plot.
        self.input_boxes = self.browser.find_elements_by_tag_name('input')
        for end_airport in user_info.end_airport:
            for start_airport in user_info.start_airport:
                # Departure Airport
                self.input_departure_airport(start_airport)

                # Arrival Airport
                self.input_arrival_airport(end_airport)

                # Departure Date
                self.input_date(user_info.date_leave)

    def select_flight_type(self, user_info):
        trip_type = self.browser.find_element_by_xpath('//button[normalize-space()="Round trip"]')
        trip_type.click()
        if user_info.flight_type == "Round Trip":
            trip_type.send_keys(Keys.ENTER)
        elif user_info.flight_type == "One-Way":
            trip_type.send_keys(Keys.DOWN, Keys.ENTER)

    def input_departure_airport(self, start_airport):
        flying_from_elem = self.input_boxes[0]
        self.browser.execute_script("arguments[0].setAttribute('value', arguments[1])", flying_from_elem, start_airport)
        flying_from_elem.click()
        self.actions.send_keys(Keys.DOWN, Keys.ENTER)
        self.actions.perform()
        time.sleep(1)

    def input_arrival_airport(self, end_airport):
        going_to_elem = self.input_boxes[2]
        self.browser.execute_script("arguments[0].setAttribute('value', arguments[1])", going_to_elem, end_airport)
        going_to_elem.click()
        self.actions.send_keys(Keys.DOWN, Keys.ENTER)
        self.actions.perform()
        time.sleep(1)

    def input_date(self, date):
        date_elem = self.input_boxes[4]
        date_elem.send_keys(Keys.CONTROL + "a", Keys.DELETE)
        date_elem.send_keys(date)
        date_elem.click()
        time.sleep(1)

    def scrape_calendar(self):
        # Get calendar info for current month
        self.get_calendar_info()

        # Best to make this number even
        months_to_search = 8

        # Set up while loop below
        total_iter = months_to_search / 2 - 1  # subtract 1 because we already searched 2 months
        counter = 0

        # Change month, get calendar information again for new month
        while counter < total_iter:
            self.change_search_date(2)
            counter += 1

            # TODO: input new data after incrementing
            self.input_date()

    def get_calendar_info(self):
        time.sleep(3)
        calendars = self.browser.find_element_by_xpath("//*[@id=\"ow59\"]/div[2]/div/div[2]/div[2]/div/div/div[1]/div")
        cal_text = calendars.text.split("\n")

        # Parse calendar text and store dates and prices
        flight_prices = []
        flight_dates = []
        month_list = []
        month_count = 0
        for ind, item in enumerate(cal_text):
            if not item.startswith("$") and len(item) > 2 and month_count <= 1:
                # TODO: Fix this condition so that it will find prices in a month that doesn't have a price on 1st day
                if cal_text[ind+9].startswith("$"):
                    month_list.append(item)
                    month_count += 1

            if item.startswith("$"):
                flight_prices.append(item.replace("$", ""))
                flight_dates.append(cal_text[ind-1])

        # TODO: Now that I can parse the info from the calendar, I need to learn how to get that data in the right
        #  format to use the plotting features.  I also need to figure out how to store it like I did with the Expedia
        #  flights.  I also think that this process will work as long as I call this function new each time I search.
        #  Then it will find the right price data for the months I want.

    def change_search_date(self, pm):
        # TODO: Fix method to work with data members I have access to
        # Increase or decrease user-input travel month
        # pm -- plus/minus, sets if you will increment or decrement month (1 or -1)

        # Get month, day, and year from initial departure date
        month = self.date_leave.split("/")[0]
        day = self.date_leave.split("/")[1]
        year = self.date_leave.split("/")[2]

        # Increment/decrement month based on pm
        new_month = int(month) + pm
        new_year = year

        # Check if increment/decrement takes the date to a different year (Dec -> Jan, Jan -> Dec)
        if new_month > 12:
            new_month -= 12
            new_year = int(year) + 1
        elif new_month < 1:
            new_month += 12
            new_year = int(year) - 1

        # ###########################################################################
        # TODO: NEED TO NOTE CURRENT MONTH SO THAT I DON'T TRY TO SEARCH IN THE PAST
        # ###########################################################################
        today = datetime.datetime.today()
        curr_month = today.month
        curr_year = today.year - 2000
        if new_month < curr_month and curr_year == new_year:
            new_month = curr_month

        # Update departure date (data member)
        self.set_date_leave(f"{new_month}" + '/' + f"{day}" + '/' + f"{new_year}")
