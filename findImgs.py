# TODO - handle the current BC (minus a day???)

# https://upload.neopets.com/beauty/images/winners/Poysion-2017-09-29.gif

import datetime

# Starting date of BC
start_date = datetime.date(2000, 11, 27)  # Year, Month, Day

def add_week(date):
    return date + datetime.timedelta(days=7)

def handle_bc_irregularities(date):
    """
    Handles irregularities with BC dates.
    For example, the date 15/01/01 BC never occurred. This function adjusts such dates to the next valid date.

    Parameters:
        date (datetime.date): The date to be checked and potentially corrected. This should be a date in the BC era.

    Returns:
        datetime.date: The corrected date, if an irregularity was found and corrected; otherwise, returns the original date.
    """
    # function implementation goes here

    adjustments = {
        datetime.date(2001, 1, 15): datetime.date(2001, 1, 22),
        datetime.date(2004, 3, 15): datetime.date(2004, 3, 22)
    }

    if date in adjustments:
        date = adjustments[date]

    return date

# Set dates to loop through
current_date = start_date
today = datetime.date.today()


# Loop through dates
while current_date <= today:
    print(current_date)

    # Adjust date if it's an irregular case
    current_date = handle_bc_irregularities(current_date)

    # Move to the next week
    current_date += datetime.timedelta(days=7)