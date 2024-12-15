"""Configuration settings for the Bethpage tee time booking bot."""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Credentials
EMAIL = os.getenv('BETHPAGE_EMAIL')
PASSWORD = os.getenv('BETHPAGE_PASSWORD')

# URLs
BASE_URL = "https://foreupsoftware.com/index.php/booking/19/2674"
LOGIN_URL = f"{BASE_URL}#/login"

# Timing Configuration
BOOKING_HOUR = 19  # 7 PM
BOOKING_MINUTE = 0
DAYS_IN_ADVANCE = 7

# Tee Time Preferences
WEEKEND_DAYS = [5, 6]  # Saturday and Sunday (0 = Monday, 6 = Sunday)
EARLIEST_TEE_TIME = "06:00"  # Earliest acceptable tee time
LATEST_TEE_TIME = "11:00"   # Latest acceptable tee time
PREFERRED_COURSES = ["Bethpage Black Course", "Bethpage Red Course"]

# Selenium Configuration
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '/usr/local/bin/chromedriver')
IMPLICIT_WAIT = 10
PAGE_LOAD_TIMEOUT = 30

# Booking Attempt Configuration
MAX_RETRIES = 3
RETRY_DELAY = 0.5  # seconds
