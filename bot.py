"""Bethpage tee time booking bot implementation."""
from datetime import datetime, timedelta
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import config

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='bethpage_bot.log'
)

class BethpageBot:
    def __init__(self):
        """Initialize the bot with configuration settings."""
        self.driver = None
        self.setup_driver()
        self.logged_in = False

    def setup_driver(self):
        """Configure and initialize the Selenium WebDriver."""
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(config.IMPLICIT_WAIT)
        self.driver.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)

    def login(self):
        """Log into the booking system."""
        try:
            self.driver.get(config.LOGIN_URL)

            # Wait for login form
            login_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )

            # Find and fill email field
            email_field = self.driver.find_element(By.NAME, "email")
            email_field.clear()
            email_field.send_keys(config.EMAIL)

            # Find and fill password field
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(config.PASSWORD)

            # Submit login form
            login_button.click()

            # Wait for successful login
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".tee-time-search"))
            )

            self.logged_in = True
            logging.info("Successfully logged in")

        except Exception as e:
            logging.error(f"Login failed: {str(e)}")
            raise

    def is_good_tee_time(self, time_str, course_name):
        """
        Determine if a tee time is desirable based on configuration preferences.

        Args:
            time_str (str): The tee time in HH:MM format
            course_name (str): Name of the golf course

        Returns:
            bool: True if the tee time meets preferences, False otherwise
        """
        try:
            tee_time = datetime.strptime(time_str, "%H:%M").time()
            earliest = datetime.strptime(config.EARLIEST_TEE_TIME, "%H:%M").time()
            latest = datetime.strptime(config.LATEST_TEE_TIME, "%H:%M").time()

            # Check if time is within preferred range
            if not (earliest <= tee_time <= latest):
                return False

            # Check if course is preferred
            if course_name not in config.PREFERRED_COURSES:
                return False

            return True

        except ValueError:
            logging.error(f"Invalid time format: {time_str}")
            return False

    def book_tee_time(self, target_date):
        """
        Attempt to book a tee time for the specified date.

        Args:
            target_date (datetime): The date to book

        Returns:
            bool: True if booking was successful, False otherwise
        """
        try:
            if not self.logged_in:
                self.login()

            # Navigate to booking page for target date
            booking_url = f"{config.BASE_URL}#/teetimes?date={target_date.strftime('%Y-%m-%d')}"
            self.driver.get(booking_url)

            # Wait for tee times to load
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "tee-time-item"))
            )

            # Find all available tee times
            tee_time_elements = self.driver.find_elements(By.CLASS_NAME, "tee-time-item")

            for element in tee_time_elements:
                time_str = element.find_element(By.CLASS_NAME, "time").text
                course_name = element.find_element(By.CLASS_NAME, "course-name").text

                if self.is_good_tee_time(time_str, course_name):
                    # Click to select the tee time
                    element.click()

                    # Wait for booking confirmation button
                    confirm_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "button.confirm-booking"))
                    )
                    confirm_button.click()

                    logging.info(f"Successfully booked tee time: {time_str} at {course_name}")
                    return True

            logging.info("No suitable tee times found")
            return False

        except Exception as e:
            logging.error(f"Error booking tee time: {str(e)}")
            return False

    def wait_for_booking_window(self, target_date):
        """
        Wait until the booking window opens for the target date.

        Args:
            target_date (datetime): The date to book
        """
        booking_time = datetime.now().replace(
            hour=config.BOOKING_HOUR,
            minute=config.BOOKING_MINUTE,
            second=0,
            microsecond=0
        )

        while datetime.now() < booking_time:
            time.sleep(0.1)  # Short sleep to prevent CPU spinning

        logging.info(f"Booking window open for {target_date}")

    def cleanup(self):
        """Clean up resources."""
        if self.driver:
            self.driver.quit()
