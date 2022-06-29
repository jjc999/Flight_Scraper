from userData import userData
from Selenium_Flight_Scraper_Tool import seleniumFS

# -----------------
# Gather User Data
# -----------------
user = userData()
# user.get_user_data() # print user data to confirm I got it correctly

# -----------------------------
# Use Selenium to open browser
# -----------------------------
SFS = seleniumFS()
SFS.open_browser()
SFS.input_user_data(user)