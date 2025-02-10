import re
from datetime import datetime
from dateutil.relativedelta import relativedelta

# Function to parse relative time strings like "2 days ago", "1 month ago", etc.
def parse_relative_time(time_str):
    """
    Parses a relative time string (e.g., "2 days ago", "1 month ago") and converts it into an absolute datetime.

    Args:
        time_str (str): A string representing the relative time (e.g., "2 days ago", "3 months ago").

    Returns:
        datetime: The datetime object representing the time relative to the current date and time.
        None: If the time string does not match the expected format.
    """
    # Get the current date and time
    now = datetime.now()

    # Regular expression to match the time format like '2 days ago', '1 month ago', etc.
    # It looks for a number followed by a unit of time (e.g., days, months, years)
    time_regex = r'(\d+)\s*(days?|hours?|months?|years?)\s*ago'

    # Try to match the time string with the regex
    match = re.match(time_regex, time_str.lower())

    # If a match is found, proceed to extract the value and unit (days, months, etc.)
    if match:
        value = int(match.group(1))  # Extract the number (e.g., 2 for "2 days ago")
        unit = match.group(2)  # Extract the unit (e.g., 'days', 'hours', etc.)

        # Now, check which unit was found and calculate the new date by subtracting the value from the current date
        if 'day' in unit:
            # If it's a "day" or "days", subtract the corresponding number of days from the current date
            return now - relativedelta(days=value)
        elif 'hours' in unit:
            # If it's an "hour" or "hours", subtract the corresponding number of hours from the current time
            return now - relativedelta(hours=value)
        elif 'month' in unit:
            # If it's a "month" or "months", subtract the corresponding number of months from the current date
            return now - relativedelta(months=value)
        elif 'year' in unit:
            # If it's a "year" or "years", subtract the corresponding number of years from the current date
            return now - relativedelta(years=value)

    # If no match is found (i.e., the string isn't in a valid format), return None
    return None
