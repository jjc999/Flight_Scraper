# Flight_Scraper

This program is designed to allow users to search a wide variety of trips over a range of dates to determine flight statistics (prices, best times to fly, etc.).  The tool gathers the flight data from Google Flights.  


Here is an overview of the process:

1. Gather the search information from the user (dates, airports, etc.) in the terminal.  This data is stored in the userData class.
2. Retrieve the flight data from Google Flights based on the user's inputs.  The Selenium package is used to interact with the browser and gather the data.  The googleFS class uses Selenium to interact with the Google Flights page to gather the data.
   a. First need to be able to open the browser using Selenium.
   b. Next you need all of the xpaths for each box and button on the website so the user data can be entered in to those places. 
3. Once the flight data can be accessed (hopefully from the calendar on the main search page), the results are stored in the flightData class.  This class is a custom container that allows you to store the flight data with the corresponding day and month for plotting and analysis.

TODO
- Build the userData class and methods
  - Decide what the data members should be
  - Write the method that collects the data from the user in the terminal.  Could this just be in the constructor?
- Use Selenium to input the user data into the browser
  - Make sure I can use Selenium in replit.
  - Figure out the xPaths for each of the spots on the website (learn how to access the things I need)
  - Build the general structure of the googleFS class
    - Define data members for xPaths
    - An instance of userData should either be a data member or passed to the constructor