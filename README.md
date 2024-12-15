# Bethpage Tee Time Booking Bot

This bot automates the process of booking tee times at Bethpage State Golf Course for weekend slots. It's designed to quickly secure tee times when they become available at 7 PM, 7 days in advance.

## Features

- Automatically books tee times for Saturdays and Sundays
- Targets the 7 PM release window (7 days in advance)
- Configurable preferences for acceptable tee times
- Automatic login with stored credentials
- Logging system for tracking booking attempts
- Retry mechanism for failed booking attempts

## Setup

1. Install dependencies:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure credentials:
The bot will automatically create a `.env` file with your credentials on first run.

3. Adjust preferences in `config.py`:
- Modify `EARLIEST_TEE_TIME` and `LATEST_TEE_TIME` for preferred time slots
- Update `PREFERRED_COURSES` list for course preferences

## Usage

Run the bot:
```bash
python main.py
```

The bot will:
1. Wait for the 7 PM booking window
2. Attempt to book tee times for the next available weekend
3. Retry failed booking attempts
4. Log all activities to `bethpage_bot.log`

## Requirements

- Python 3.8+
- Chrome/Chromium browser
- ChromeDriver (matching your Chrome version)
