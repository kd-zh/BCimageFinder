import httpx
import asyncio
import datetime

#! -------- Set constants --------

# Starting date of BC (Monday)
START_DATE = datetime.date(2000, 11, 27)  # Year, Month, Day

# Base URL for BC winners
URL_BASE ="https://upload.neopets.com/beauty/images/winners/"

# The BC to the best of my knowledge only allows these
FILE_EXTENSIONS = [".jpg", ".gif"]

# Set petname to loop through
PETNAME = "Poysion"

TODAY = datetime.date.today()


#! -------- Define functions --------

def handle_bc_irregularities(date: datetime.date):
    """
    Handles irregularities with BC dates.
    For example, the 15/01/01 BC never occurred. This function adjusts such dates to the next valid date.

    Parameters:
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

    Parameters:
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


#! -------- Start Logic --------
        
# Set dates to loop through
current_date = closest_friday(START_DATE)

# Initialise a list to store all potential URLs
valid_urls = []

# Initialise list to store BC entries (valid URLs)
bc_entries = []

# Debugging
START_DATE = datetime.date(2016, 9, 3)
current_date = closest_friday(START_DATE)

TODAY = closest_friday(TODAY)

# Loop through all given dates
while current_date <= TODAY:
    print(current_date)

    # Adjust date if it's an irregular case
    current_date = handle_bc_irregularities(current_date)

    # Move to the next week
    current_date += datetime.timedelta(days=7)

    for ext in FILE_EXTENSIONS:
        current_date_url = URL_BASE + PETNAME + "-" + str(current_date) + ext
        valid_urls.append(current_date_url)

print("Number of valid URLS: ", len(valid_urls))

async def batch_check_urls(urls, batch_size=10):
    # Process the URLs in batches
    results = []

    for i in range(0, len(urls), batch_size):
        batch = urls[i:i + batch_size]
        tasks = [asyncio.create_task(check_url(url)) for url in batch]
        results += await asyncio.gather(*tasks, return_exceptions=True)
        print("URLs scanned: ", i)

    return results

results = asyncio.run(batch_check_urls(valid_urls))

print(bc_entries)