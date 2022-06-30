# This is the class that utilizes Selemium to gather the data based on the user inputs (data collected in userData class) from google flights.  This includes storing the xPath (or related) data for each of the fields on the website.  The purpose of this class is to simply build the tools needed to access the flight data from google flights using Selenium.

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time

class seleniumFS:
  def __init__(self):
    # Configure browser and to be able to open chrome
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    self.browser = webdriver.Chrome('chromedriver', options=chrome_options) # This is the path when using replit
    self.google_flights_url = "https://www.google.com/travel/flights"

    # Dictionary of xPaths for google flights website
    self.xPaths = {'departure_airport': "//*[@id='ow44']/div[1]/div/div/input"}

  def open_browser(self):
    self.browser.get(self.google_flights_url)

  def input_user_data(self, user):
    # departure_airport_elem = self.browser.find_element("xpath", self.xPaths['departure_airport'])
    departure_airport_elem = self.browser.switch_to.active_element;
    departure_airport_elem.clear()
    departure_airport_elem.send_keys(user.departure_airport)
    time.sleep(5)
    # TODO: input user data at this xPath (note that the xPath I am using now might not be correct) using Keys.  In other words, I need to confirm that I have the right xPath and actually input the user data onto the page using Keys.