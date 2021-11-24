from Flights import Flights
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import requests
from bs4 import BeautifulSoup


class GoogleFlights_Sandbox(Flights):
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
        start_airport = input('From: ')
        end_airport = input('To: ')
        flight_type = input('Flight Type (Round Trip/One-Way): ')
        start_date = input('Departing on (MM/DD/YY): ')
        if flight_type == 'Round Trip':
            end_date = input('Returning on (MM/DD/YY): ')
        else:
            end_date = ''

        # Compile user search info into list
        user_search = [start_airport, end_airport, flight_type, start_date, end_date]
        print(user_search)
        self.search(user_search)

    def search(self, user_search):
        # Method to actually search google flights based on user inputs
        browser = webdriver.Chrome('C:\\Users\\byufa\\PycharmProjects\\SeleniumChromeDriver\\chromedriver')
        url = "https://www.google.com/flights?hl=en#flt=/m/0f2r6..2020-05-28*./m/0f2r6.2020-06-01;c:USD;e:1;ls:1w;sd:0;t:h"
        browser.get(url)

        # Try selecting drop down item
        flight_type_xpath = "//*[@id=\"flt-app\"]/div[2]/main[1]/div[4]/div/div[3]/div/div[1]/div[1]/dropdown-menu"
        flight_type_elem = browser.find_element_by_xpath(flight_type_xpath)
        select = Select(flight_type_elem)

        # elem = browser.find_element_by_link_text('Where To?')
        # elem.click()

        # Click on destination box.  First need to find it
        result = requests.get(url)
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')
        suggested_search = soup.find_all("span", class_="\"gws-flights-form__text-field-placeholder\"")
        print(suggested_search.style)



        # # destination_xpath = "/html/body/div[2]/div[2]/div/div[2]/div[3]/div/jsl/div/div[5]/div/destination-picker/div[1]/div[2]/div[2]/input"
        # destination_xpath = "//*[@id=\"flt-app\"]/div[2]/main[1]/div[4]/div/div[3]/div/div[2]/div[2]/div[2]/input"
        # # select_destination = browser.find_element_by_class_name(""gws-flights-form__text-field-placeholder"")
        # select_destination.click()
        # input_xpath = "//*[@id=\"sb_ifc50\"]/input"
        # destination_box = browser.find_element_by_xpath(input_xpath)  # only works if you click on the text box
        # destination_box.clear()
        # destination_box.send_keys("Rome")
        # destination_box.send_keys(Keys.ENTER)
        #
        # from_box = browser.find_element_by_xpath(input_xpath)
        # from_box.clear()
        # from_box.send_keys("SLC")
        # from_box.send_keys(Keys.ENTER)
        # # destination_box = browser.find_element_by_class_name('gws-flights-form__text-field-placeholder')
        # # destination_box.click()


