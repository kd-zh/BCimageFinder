import time
import httpx
import asyncio
import datetime


#! -------- Changeable Variables --------

# Set petname to loop through (case-sensitive)
PETNAME = "Isap"

# Set the number of trophies your pet has
NUM_IMG_EXPECTED = 1

# Set how old your Neopet is (in hours)
HOURS = 112946


#! -------- Set constants --------

# Find elapsed time
START_TIME = time.time()

# Starting date of BC (Monday)
START_DATE = datetime.date(2000, 11, 27)  # Year, Month, Day
current_date = START_DATE # current as in the current date being looped through

# Today's date
TODAY = datetime.date.today()
end_date = TODAY

# Base URL for BC winners
URL_BASE ="https://upload.neopets.com/beauty/images/winners/"

# The BC to the best of my knowledge only allows these
FILE_EXTENSIONS = [".jpg", ".gif"]


#! -------- Define functions --------

def handle_bc_irregularities(date: datetime.date):
    """
    Handles irregularities with BC dates.
    For example, the 15/01/01 BC never occurred. This function adjusts such dates to the next valid date.

    Parameter:
        date (datetime.date): The date to be checked and potentially corrected.

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

def closest_friday(date: datetime.date):
    """
    Winners are announced on the Friday, so make sure all dates in the URL are fridays
    Handles invalid dates (dates in the future and dates before 01/12/00 the first friday)

    Parameter:
        date (datetime.date): The date to be checked and potentially corrected.

    Returns:
        datetime.date: The corrected date, if it was an invalid date or not a Friday; otherwise, returns the original date.
    """

    # Check the day of the week (0 is Monday, 6 is Sunday)
    day_of_week = date.weekday()

    # If it's already Friday, return the date
    if day_of_week == 4:
        return date

    # Calculate the difference to the previous and next Friday
    days_to_prev_friday = (day_of_week - 4) % 7
    days_to_next_friday = (4 - day_of_week) % 7

    # If next friday is in the future, choose last friday
    if date > TODAY:
        ## Recursion is the devil's technique! We avoid it.
        # Check the day of the week for today
        day_of_week = TODAY.weekday()

        # Calculate the difference to the previous Friday
        days_to_prev_friday = (day_of_week - 4) % 7

        return TODAY - datetime.timedelta(days=days_to_prev_friday)
    
    # If the date was in the non-BC past, we manually adjust to the first BC date.
    elif date < datetime.date(2000, 12, 1):
        return datetime.date(2000, 12, 1)
    
    # Otherwise determine which is closer, the previous or next Friday
    else: 
        if days_to_prev_friday < days_to_next_friday:
            return date - datetime.timedelta(days=days_to_prev_friday)
        else:
            return date + datetime.timedelta(days=days_to_next_friday)

async def check_url(url):
    """
    Checks URLs to see if it contains a BC image. If it doesn't exist (status code is not 200) then there was no image.

    Parameter:
        url (string): The url to be checked.

    Returns:
        string: Whether or not the URL contains an image
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            if response.status_code == 200:
                bc_entries.append(url)
                return f"URL {url} is valid and returns an image."
            else:
                return f"URL {url} returned a status code of {response.status_code}."
        except httpx.RequestError as e:
            return f"URL {url} resulted in an error: {e}"

async def batch_check_urls(urls, batch_size=10):
    """
    Process the URLs in batches to prevent sending too many requests to Neopets.

    Parameters:
        url (string): The url to be checked.
        batch_size (int, optional): The number of URLs checked in each batch.
    """

    results = []

    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        tasks = [asyncio.create_task(check_url(url)) for url in batch]
        results += await asyncio.gather(*tasks, return_exceptions=True)
        print("URLs scanned: ", i, "/", len(urls), " | BC Images Found: ", len(bc_entries))
        if len(bc_entries) == NUM_IMG_EXPECTED:
            break

    return results


#! -------- Start Logic --------

# Current date and time in NST (GMT-8)
current_date_gmt8 = datetime.datetime.utcnow() - datetime.timedelta(hours=8)

# Corresponding date before the given number of hours
current_date = current_date_gmt8 - datetime.timedelta(hours=HOURS)
current_date = current_date.date()

# Clean to grab the closest Friday (when winners are announced)
current_date = closest_friday(current_date)
end_date = closest_friday(end_date)

# Initialise a list to store all potential URLs
valid_urls = []

# Initialise list to store BC entries (valid URLs)
bc_entries = []

# Loop through all given dates
while current_date <= end_date:

    # Adjust date if it's an irregular case
    current_date = handle_bc_irregularities(current_date)

    # Move to the next week
    current_date += datetime.timedelta(days=7)

    for ext in FILE_EXTENSIONS:
        current_date_url = URL_BASE + PETNAME + "-" + str(current_date) + ext
        valid_urls.append(current_date_url)

print("Number of valid URLS: ", len(valid_urls))

results = asyncio.run(batch_check_urls(valid_urls))

print(len(bc_entries), " image(s) were found.")

print(bc_entries)

END_TIME = time.time()

ELAPSED_TIME = END_TIME - START_TIME

TIME_PER_URL = ELAPSED_TIME/len(valid_urls)

print("Time taken per URL: ", TIME_PER_URL)