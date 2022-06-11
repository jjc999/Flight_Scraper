# Flight_Scraper

This program is designed to allow users to search a wide variety of trips over a range of dates to determine flight statistics (prices, best times to fly, etc.).  The tool gathers the flight data from Google Flights.  

Here is an overview of the process:

1. Gather the search information from the user (dates, airports, etc.) in the terminal.  This data is stored in the userData class.
2. Retrieve the flight data from Google Flights based on the user's inputs.  The Selenium package is used to interact with the browser and gather the data.  The googleFS class uses Selenium to interact with the Google Flights page in a custom way to gather the data.