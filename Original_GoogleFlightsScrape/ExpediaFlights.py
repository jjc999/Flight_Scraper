from Flights import Flights
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import mplcursors
import numpy as np
import time
import datetime


class ExpediaFlights(Flights):
    def __init__(self):
        super().__init__()

    def find_flight_info(self):
        # Method that call other methods to collect all relevant flight info from Google Flights page
        # TODO:
        # Make this a pure virtual method in Flights class.  Then this must be defined in all children classes but
        # is not defined in the Flights class.
        x = 2

    def user_flight_info(self):
        # Ask the user to input the flight information they want to search
        print('///////////////////////////////')
        print('Enter in Desired Flight Info')
        print('///////////////////////////////')
        self.set_start_airport(input('From: '))
        self.set_end_airport(input('To: '))
        self.set_flight_type(input('Flight Type (Round Trip/One-Way): '))
        self.set_date_leave(input('Departing on (MM/DD/YY): '))
        self.date_leave_orig = self.date_leave
        if self.flight_type == 'Round Trip':
            self.set_date_return(input('Returning on (MM/DD/YY): '))
            self.date_return_orig = self.date_return
        else:
            self.set_date_return("")
            self.date_return_orig = self.date_return

        # If user searches multiple airports, convert search to list
        self.parse_airports()

        # Store number of flights to make plotting easier
        self.num_flights = len(self.start_airport)*len(self.end_airport)

        # Build year_price_mat
        self.build_year_price_mat()

        # Start search
        self.search()

    def search(self):
        # Method to search Expedia based on user inputs
        url_bool = False

        # TODO: Make the code able to parse either webpage
        while not url_bool:
            browser = webdriver.Chrome('C:\\Users\\byufa\\PycharmProjects\\SeleniumChromeDriver\\chromedriver')
            url = "https://www.expedia.com/Flights"
            browser.get(url)
            time.sleep(2)
            try:
                check_site = browser.find_element_by_xpath("//*[@id=\"flight-origin-flp\"]")
                url_bool = True
            except:
                url_bool = False
                browser.quit()

        # Select Flight Type, Input Dates, and starting and ending airports
        flight_type_elem = []
        depart_elem = []
        if self.flight_type == "Round Trip":
            flight_type_elem = browser.find_element_by_id("flight-type-roundtrip-label-flp")
            depart_elem = browser.find_element_by_id("flight-departing-flp")
            return_elem = browser.find_element_by_id("flight-returning-flp")
            return_elem.send_keys(self.date_return)
        elif self.flight_type == "One-Way":
            flight_type_elem = browser.find_element_by_id("flight-type-one-way-label-flp")
            depart_elem = browser.find_element_by_id("flight-departing-single-flp")

        # Search for each combination of starting and ending airports the user input
        # TODO: Need to update call to scrape_calendar (and method itself) to handle multiple airport searches
        # TODO: This includes plotting the correct data, storing the data for each airport combination correctly,
        # TODO: resetting the dates for each search, and plotting all the curves on the same plot.
        for end_airport in self.end_airport:
            for start_airport in self.start_airport:
                # Departure Airport
                flying_from_elem = browser.find_element_by_xpath("//*[@id=\"flight-origin-flp\"]")
                flying_from_elem.clear()
                flying_from_elem.send_keys(start_airport)
                time.sleep(1)

                # Select Flight Type
                flight_type_elem.click()

                # Date
                depart_elem.send_keys(self.date_leave)
                time.sleep(1)

                # Arrival Airport
                going_to_elem = browser.find_element_by_xpath("//*[@id=\"flight-destination-flp\"]")
                going_to_elem.clear()
                going_to_elem.send_keys(end_airport)
                time.sleep(1)

                # Click on date again to generate calendar for desired month
                depart_elem.click()

                # Scrape prices from calendar (only if One-Way flight)
                if self.flight_type == "One-Way":
                    self.scrape_calendar(browser)

                    # Plot Results and increment flight_ind
                    # self.plot_prices(start_airport, end_airport)
                    self.plot_prices_new(start_airport, end_airport)
                    self.flight_ind += 1
                    self.flight_ind += 1

                    # Store prices and dates in matrix
                    self.date_mat.append(self.date_list)
                    self.price_mat.append(self.price_list)
                    self.dates_length_mat.append(self.dates_length_list)

                    # Reset price and date lists for next starting/ending airport combo
                    self.price_list = []
                    self.date_list = []
                    self.dates_length_list = []

                    # Reset departure date (in data member and on page)
                    self.date_leave = self.date_leave_orig
                    depart_elem.clear()

        # Plot all prices on one plot
        # TODO: Make sure this if statement condition is correct
        if len(self.start_airport) > 1 or len(self.end_airport) > 1:
            self.plot_all_flights()

        # Submit search
        time.sleep(1)
        depart_elem.send_keys(Keys.ENTER)

        # Collect Prices
        self.scrape_prices(browser.current_url, browser)

    def scrape_prices(self, current_url, browser):
        # BeautifulSoup Approach (need to pass in url from search method)
        # -----------------------
        time.sleep(15)
        prices = browser.find_elements_by_xpath("//span[@data-test-id='listing-price-dollars']")
        price_list = [value.text for value in prices]

        # airline name
        airlines = browser.find_elements_by_xpath("//span[@data-test-id='airline-name']")
        airlines_list = [value.text for value in airlines]

        # Print results
        print("--------------------------")
        print(f"Best Price -- {price_list[0]} ({airlines_list[1]})")
        print("--------------------------")
        print("")
        print('Top 5 Listings')
        print('---------------')
        for flight in range(1, 6):
            print(airlines_list[flight] + ' -- ' + price_list[flight-1])

    def scrape_calendar(self, browser):
        # Get calendar info for current month
        self.get_calendar_info(browser)

        # Best to make this number even
        months_to_search = 8

        # Set up while loop below
        total_iter = months_to_search/2 - 1  # subtract 1 because we already searched 2 months
        counter = 0

        # Change month, get calendar information again for new month
        while counter < total_iter:
            self.change_search_date(2)
            counter += 1

            # TODO: Make method that enters in user info (like departure date), then call that here to update search
            depart_elem = browser.find_element_by_id("flight-departing-single-flp")
            going_to_elem = browser.find_element_by_xpath("//*[@id=\"flight-destination-flp\"]")
            depart_elem.clear()
            depart_elem.send_keys(self.get_date_leave(1))
            time.sleep(1)
            going_to_elem.click()
            depart_elem.click()

            self.get_calendar_info(browser)

        # Store final date for later use in plotting
        self.date_leave_final = self.date_leave

    def get_calendar_info(self, browser):
        time.sleep(3)
        cal_left = browser.find_elements_by_xpath("//*[@id=\"flight-departing-wrapper-single-flp\"]/div/div[2]/div[2]/table")
        cal_right = browser.find_elements_by_xpath("//*[@id=\"flight-departing-wrapper-single-flp\"]/div/div[2]/div[3]/table")
        cal_left_str = cal_left[0].text
        cal_right_str = cal_right[0].text
        cal_str_list = [cal_left_str, cal_right_str]

        for cal_ind, cal in enumerate(cal_str_list):
            # Parse Flight Prices
            ind = 0
            flight_prices = []
            cal_list = cal.split(" ")
            for item in cal_list:
                if item.startswith("$"):
                    txt = item.split("\n")
                    for price in txt:
                        if price.startswith("$"):
                            if ind % 2:
                                flight_prices.append(price)
                                self.price_list.append(price)
                            ind += 1
            # Parse Dates
            cal_list2 = cal.split("\n")
            month = cal_list2[0]
            self.month_list.append(month)
            dates_list = []
            counter = 0
            for item in cal_list2:
                if item.startswith("P"):
                    dates_list.append(cal_list2[counter - 2].strip() + ' ' + cal_list2[counter - 1])
                    self.date_list.append(cal_list2[counter - 2].strip() + ' ' + cal_list2[counter - 1])
                counter += 1

            # Store number of flights for month
            self.dates_length_list.append(len(dates_list))

            # Print dates and prices
            # First check that we have the same number of dates as prices
            if len(dates_list) != len(flight_prices):
                print("ERROR -- different number of dates and prices")
            elif len(dates_list) == 0:
                print(f"No flights in {month}")
                self.month_list.pop()
            else:
                for flight in range(0, len(dates_list)):
                    print(dates_list[flight] + ' --- ' + flight_prices[flight])

            # Separate flight day from month to store in year_price_mat
            days_list = []
            for date in dates_list:
                days_list.append([int(day) for day in date.split() if day.isdigit()])

            # Store prices in year_price_mat based on days_list
            search_month = int(self.date_leave.split("/")[0]) + cal_ind
            for ind, day in enumerate(days_list):
                self.year_price_mat[search_month - 1][day[0] - 1].append(flight_prices[ind])

            # Fill in any blank days with []
            for days in range(0, len(self.year_price_mat[search_month-1])):
                try:
                    temp = self.year_price_mat[search_month-1][days][self.flight_ind]
                    # If empty, this will not work and we will move into the except case below
                    temp = temp + 'String'
                except:
                    self.year_price_mat[search_month-1][days].append([])

    def change_search_date(self, pm):
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

    def plot_prices(self, start_airport, end_airport):
        # Convert strings to values
        price_list = []
        for price in self.price_list:
            price_list.append(int(price.replace("$", "").replace(",", "")))

        # Find when months start and end in self.date_list
        month_start_ind = [0]
        for ind, date in enumerate(self.date_list):
            if ind > 0:
                if date[0:3] != self.date_list[ind-1][0:3]:
                    month_start_ind.append(ind)

        avg_price = np.average(price_list)

        # Plot
        fig, ax = plt.subplots()
        ax.plot(price_list, ':.')
        ax.plot([0, len(price_list)], [avg_price, avg_price], '--')
        formatter = ticker.FormatStrFormatter('$%4.2f')
        ax.yaxis.set_major_formatter(formatter)
        plt.xticks(month_start_ind, self.month_list, rotation=45)
        plt.title(f"{start_airport} --> {end_airport}")
        plt.suptitle(f"{self.flight_type}, {self.month_list[0]} - {self.month_list[-1]}", fontsize=10)

        # Allows user to see date when they hover over point
        # mplcursors.cursor(hover=True)
        # mplcursors.cursor(ax).connect("add", lambda sel: sel.annotation.set_text(self.date_list[sel.target.index]))

        # Add star to cheapest day
        ax.plot(price_list.index(min(price_list)), min(price_list), marker=(5, 1), markersize=10)

        # Legend
        plt.legend([f"{start_airport} --> {end_airport}", f"Average Price = ${round(avg_price, 2)}",
                    f"Lowest Price = ${round(np.nanmin(price_list), 2)}"])

        plt.show(block=False)

    def plot_prices_new(self, start_airport, end_airport):
        # Plot prices based on year_price_mat

        # Get starting and ending months
        start_month = int(self.date_leave_orig.split("/")[0])
        end_month = int(self.date_leave.split("/")[0]) + 1

        # TODO: Fix bug where end_month < start_month (goes past new years)
        if end_month < start_month:
            end_month += 12

        # Build month_start_ind for plotting (x axis spacing)
        month_start_ind = self.build_month_start_ind(start_month-1, end_month-1)

        # Convert price strings to values
        price_list = []
        for month in range(start_month-1, end_month):
            month_ind = month
            if month_ind > 11:
                month_ind -= 12
            month_prices = self.year_price_mat[month_ind]
            for price in month_prices:
                try:
                    price_list.append(int(price[self.flight_ind].replace("$", "").replace(",", "")))
                except:
                    price_list.append(np.nan)

        avg_price = np.nanmean(price_list)

        # Plot
        fig, ax = plt.subplots()
        ax.plot(price_list, ':.')
        ax.plot([0, len(price_list)], [avg_price, avg_price], '--')
        formatter = ticker.FormatStrFormatter('$%4.2f')
        ax.yaxis.set_major_formatter(formatter)
        plt.xticks(month_start_ind, self.month_list, rotation=45)
        plt.xlim(0, len(price_list)+1)
        plt.title(f"{start_airport} --> {end_airport}")
        plt.suptitle(f"{self.flight_type}, {self.month_list[0]} - {self.month_list[-1]}", fontsize=10)

        # Add star to cheapest day
        ax.plot(price_list.index(np.nanmin(price_list)), np.nanmin(price_list), marker=(5, 1), markersize=10)

        # TODO: Add legend that shows "SLC --> Vienna", actual average price, and lowest price
        plt.legend([f"{start_airport} --> {end_airport}", f"Average Price = ${round(avg_price, 2)}",
                    f"Lowest Price = ${round(np.nanmin(price_list), 2)}"])

        plt.show(block=False)

        # Print Flight Statistics
        print(f"{start_airport} --> {end_airport}")
        print(f"Mean Price: ${np.nanmean(price_list)}")
        print(f"Standard Deviation: ${np.nanstd(price_list)}")
        print('')

    def plot_all_flights(self):
        # Plot all flight data on one plot

        # Get starting and ending months
        start_month = int(self.date_leave_orig.split("/")[0])
        end_month = int(self.date_leave_final.split("/")[0]) + 1

        # Fix bug where end_month < start_month (goes past new years)
        if end_month < start_month:
            end_month += 12

        # Build month_start_ind for plotting (x axis spacing)
        month_start_ind = self.build_month_start_ind(start_month-1, end_month-1)

        # Set up figure
        fig, ax = plt.subplots()
        plt.title(f"{self.start_airport} --> {self.end_airport}")
        plt.suptitle(f"{self.flight_type}, {self.month_list[0]} - {self.month_list[-1]}", fontsize=10)

        # TODO: Fix bug where end_month < start_month (goes past new years) -- did this in plot_prices_new
        # Pull out prices from year_price_mat and plot
        cheapest_prices = np.zeros(((end_month-start_month+1), self.num_flights))

        for flight in range(0, self.num_flights):
            # Convert price strings to values
            price_list = []
            for month in range(start_month - 1, end_month):
                month_ind = month
                if month_ind > 11:
                    month_ind -= 12
                month_prices = self.year_price_mat[month_ind]
                key = 0
                for ind, price in enumerate(month_prices):
                    try:
                        price_val = int(price[flight].replace("$", "").replace(",", ""))
                        price_list.append(price_val)

                        # TODO: Make sure I am storing this data correctly
                        # Find and store cheapest price for that month and flight
                        if key == 0 and not np.isnan(price_val):
                            cheapest_prices[month - (start_month - 1)][flight] = price_val
                            key = 1
                        elif ind > 0 and price_val < cheapest_prices[month - (start_month - 1)][flight]:
                            cheapest_prices[month-(start_month-1)][flight] = price_val
                    except:
                        price_list.append(np.nan)

            ax.plot(price_list, ':.')

        # Format plot
        formatter = ticker.FormatStrFormatter('$%4.2f')
        ax.yaxis.set_major_formatter(formatter)
        plt.xticks(month_start_ind, self.month_list, rotation=45)
        plt.xlim(0, len(price_list) + 1)

        # Build legend and title
        legend_str = []
        for start_ind, start in enumerate(self.start_airport):
            for final_ind, final in enumerate(self.end_airport):
                legend_str.append(f"{start} --> {final}")
        plt.legend(legend_str)

        plt.show(block=False)

        # Bar plot of best prices for each flight
        # ----------------------------------------
        # Set bar plot spacing on x axis
        bar_width = 0.2
        bar_spacing = 0
        x_axis = np.arange(1, (end_month-start_month+2))

        # Build plot
        bar_fig, bar_ax = plt.subplots()
        for flight in range(0, self.num_flights):
            bar_spacing = bar_spacing + ((-1)**flight)*flight*bar_width
            bar_ax.bar(x_axis + bar_spacing, cheapest_prices[:, flight], width=bar_width)

        # Format plot
        formatter = ticker.FormatStrFormatter('$%4.2f')
        bar_ax.yaxis.set_major_formatter(formatter)
        plt.xticks(x_axis, self.month_list[0:(end_month-start_month+1)], rotation=45)
        plt.title("Cheapest Flights for Each Month")
        plt.legend(legend_str)

        plt.show(block=False)

    def parse_airports(self):
        # Convert multiple airports or keywords to list of airports for the search algorithm to process

        # Arrival Airport
        if "," in self.end_airport:
            self.end_airport = self.end_airport.split(",")
        elif self.end_airport == "Western USA":
            self.end_airport = ["SLC", "Las Vegas", "LAX", "OAK", "SFO", "Seattle"]
        elif self.end_airport == "Western Europe":
            self.end_airport = ["London", "Paris", "Dublin", "Berlin", "Rome"]
        else:
            self.end_airport = [self.end_airport]

        # Departure Airport
        if "," in self.start_airport:
            self.start_airport = self.start_airport.split(",")
        elif self.start_airport == "Western USA":
            self.start_airport = ["SLC", "Las Vegas", "LAX", "OAK", "SFO", "Seattle"]
        elif self.start_airport == "Western Europe":
            self.start_airport = ["London", "Paris", "Dublin", "Berlin", "Rome"]
        else:
            self.start_airport = [self.start_airport]

    def build_year_price_mat(self):
        for month in range(0, 12):
            if month == 0 or month == 2 or month == 4 or month == 6 or month == 7 or month == 9 or month == 11:
                self.year_price_mat[month] = [[] for day in range(0, 31)]
            elif month == 1:
                self.year_price_mat[month] = [[] for day in range(0, 29)]
            elif month == 3 or month == 5 or month == 8 or month == 10:
                self.year_price_mat[month] = [[] for day in range(0, 30)]

    def build_month_start_ind(self, start_month, end_month):
        month_start_ind = [0]
        for ind, month in enumerate(range(start_month, end_month)):
            month = month % 12
            if month == 0 or month == 2 or month == 4 or month == 6 or month == 7 or month == 9 or month == 11:
                month_start_ind.append(month_start_ind[ind] + 31)
            elif month == 1:
                month_start_ind.append(month_start_ind[ind] + 29)
            elif month == 3 or month == 5 or month == 8 or month == 10:
                month_start_ind.append(month_start_ind[ind] + 30)

        return month_start_ind
