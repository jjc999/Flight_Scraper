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
    self.xPaths = {'departure_airport': "//*[@id='i14']/div[6]/div[2]/div[2]/div[1]/div/input",
                   'arrival_airport': "//*[@id='i14']/div[6]/div[2]/div[2]/div[1]/div/input"}

  def open_browser(self):
    self.browser.get(self.google_flights_url)

  def input_user_data(self, user):
    # Recent Progress and thoughts
    # -----------------------------
    # I figured out that the departure airport box is the default active element, so I can just click on that to be able to input text.  Once I click on it, I am able to get to the text element that I can actually use Selenium to interact with (what the xpath now references).  Once I get that, I can send the departure airport text to the box.  I then click ENTER to return to the search page and then hit TAB to move over to the arrival airport box.  My strategy now is to try finding the xpaths for each element following this approach and to google around and see if other people have done this and can just give me the xpaths.
    # -----------------------------
    # Enter depature airport
    departure_airport_box = self.browser.switch_to.active_element  # Departure Airport box
    departure_airport_box.click()  # Click box to be able to input text
    departure_airport_text = self.browser.find_element("xpath", self.xPaths['departure_airport'])
    departure_airport_text.send_keys(user.departure_airport)
    departure_airport_text.send_keys(Keys.ENTER)
    departure_airport_box.send_keys(Keys.TAB)  # Move over to arrival airport box

    # Enter arrival airport
    arrival_airport_box = self.browser.switch_to.active_element
    arrival_airport_box.click()
    arrival_airport_text = self.browser.find_element("xpath", self.xPaths['arrival_airport'])
    arrival_airport_text.send_keys(user.arrival_airport)
    arrival_airport_text.send_keys(Keys.ENTER)
    arrival_airport_box.send_keys(Keys.TAB)  # Move over to date box

    # Enter dates

    # Enter flight type (only need to change to One-Way)
    # if user.flight_type == 'One-Way':
      # TODO: Learn how to change flight type using the dropdown
      
    time.sleep(10)