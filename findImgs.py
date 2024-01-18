# TODO - handle the current BC (minus a day???)

import datetime
import requests

# Starting date of BC
start_date = datetime.date(2000, 11, 27)  # Year, Month, Day

# The BC to the best of my knowledge only allows these
FILE_EXTENSIONS = [".jpg", ".gif"]

URL_BASE ="https://upload.neopets.com/beauty/images/winners/"

# Set petname to loop through
PET_NAME = "Poysion"

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

bc_entries = []
def check_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            bc_entries.append(url)
            return "URL is valid and returns a resource."
        # else:
        #     return f"URL returned a status code of {response.status_code}."
    except requests.RequestException as e:
        return f"An error occurred: {e}"

# This requests library is so slow!
start_date = datetime.date(2015, 11, 27)

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

    for ext in FILE_EXTENSIONS:
        current_date_url = URL_BASE + PET_NAME + "-" + str(current_date) + ext
        check_url(current_date_url)

print(bc_entries)