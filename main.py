"""Main script to run the Bethpage tee time booking bot."""
import logging
from datetime import datetime, timedelta
import os
import sys
from dotenv import load_dotenv
from bot import BethpageBot
import config
print("test")
logging.basicConfig(level=print)

def create_env_file():
    """Create .env file with credentials if it doesn't exist."""
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write(f'BETHPAGE_EMAIL="{os.environ.get("BETHPAGE_EMAIL", "frmccann97@gmail.com")}"\n')
            f.write(f'BETHPAGE_PASSWORD="{os.environ.get("BETHPAGE_PASSWORD", "chq8fpe*qfq*phk0YQA")}"\n')

def get_next_booking_dates():
    """
    Get the next Saturday and Sunday dates that will be available for booking.

    Returns:
        list: List of datetime objects for the next bookable weekend days
    """
    today = datetime.now()
    booking_dates = []

    # Look ahead config.DAYS_IN_ADVANCE + 7 days to find next weekend days
    for i in range(config.DAYS_IN_ADVANCE, config.DAYS_IN_ADVANCE + 7):
        future_date = today + timedelta(days=i)
        # Check if it's a weekend day (5 = Saturday, 6 = Sunday)
        if future_date.weekday() in config.WEEKEND_DAYS:
            booking_dates.append(future_date)

    return booking_dates

def test_mode():
    """Run the bot in test mode to verify core functionality."""
    print("Starting Bethpage booking bot in TEST MODE")

    try:
        bot = BethpageBot(test_mode=True)
        test_passed = bot.run_tests()

        if test_passed:
            print("All tests passed successfully!")
        else:
            print("Some tests failed. Check logs for details.")

    except Exception as e:
        print(f"Error in test mode: {str(e)}")
    finally:
        if 'bot' in locals():
            bot.cleanup()

def main():
    """Main function to run the booking bot."""
    if len(sys.argv) > 1 and sys.argv[1] == "--test":

        test_mode()
    else:
        print("Starting Bethpage booking bot")
        bot = None
        # Create .env file with credentials
        create_env_file()

        # Load environment variables
        load_dotenv()

        try:
            bot = BethpageBot()

            # Get next weekend dates to book
            booking_dates = get_next_booking_dates()

            for target_date in booking_dates:
                print(f"Preparing to book tee time for {target_date.strftime('%Y-%m-%d')}")

                # Wait for the booking window to open
                bot.wait_for_booking_window(target_date)

                # Attempt booking with retries
                for attempt in range(config.MAX_RETRIES):
                    if bot.book_tee_time(target_date):
                        break
                    print(f"Booking attempt {attempt + 1} failed, retrying...")

        except Exception as e:
            print(f"Error in main: {str(e)}")
        finally:
            if bot is not None:
                bot.cleanup()
            else:
                print("Bot instance is None, unable to cleanup")

if __name__ == "__main__":
    print("Starting main")
    main()
    print("Finished main")
