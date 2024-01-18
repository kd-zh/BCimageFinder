import httpx
import asyncio
import datetime


# Starting date of BC (Monday)
start_date = datetime.date(2000, 11, 27)  # Year, Month, Day

# Base URL for BC winners
URL_BASE ="https://upload.neopets.com/beauty/images/winners/"

# The BC to the best of my knowledge only allows these
FILE_EXTENSIONS = [".jpg", ".gif"]

# Set petname to loop through
PET_NAME = "Poysion"

TODAY = datetime.date.today()

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

# async def check_url(url):
#     async with httpx.AsyncClient() as client:
#         try:
#             response = await client.get(url)
#             if response.status_code == 200:
#                 bc_entries.append(url)
#                 return f"URL {url} is valid and returns a resource."
#             # else:
#             #     return f"URL {url} returned a status code of {response.status_code}."
#         except httpx.RequestError as e:
#             return f"URL {url} resulted in an error: {e}"

# import requests
# def check_url(url): 
#     """
#         DEFUNCT - import requests version
#     """
#     try:
#         response = requests.get(url)
#         if response.status_code == 200:
#             bc_entries.append(url)
#             return "URL is valid and returns a resource."
#         else:
#             return f"URL returned a status code of {response.status_code}."
#     except requests.RequestException as e:
#         return f"An error occurred: {e}"
        
# Set dates to loop through
current_date = closest_friday(start_date)

# Initialise a list to store all potential URLs
valid_urls = []

# Initialise list to store BC entries (valid URLs)
bc_entries = []

# Debugging
start_date = datetime.date(2024, 9, 3)
start_date = closest_friday(start_date)
print(start_date)
TODAY = datetime.date(2017, 10, 22)

# Loop through all given dates
while current_date <= today:
    print(current_date)

    # Adjust date if it's an irregular case
    current_date = handle_bc_irregularities(current_date)
    # Move to the next week
    current_date += datetime.timedelta(days=7)

    for ext in FILE_EXTENSIONS:
        current_date_url = URL_BASE + PET_NAME + "-" + str(current_date) + ext
        valid_urls.append(current_date_url)

print(valid_urls)

# async def batch_check_urls(urls):
#     tasks = [check_url(url) for url in urls]
#     return await asyncio.gather(*tasks)

# # List of URLs to check
# urls = [
#     "https://upload.neopets.com/beauty/images/winners/Poysion-2017-09-29.gif",
#     "https://upload.neopets.com/beauty/images/winners/Poysion-2017-09-29.jpg",
# ]

# results = asyncio.run(batch_check_urls(valid_urls))
# for result in results:
#     print(result)

# print(bc_entries)
        

        