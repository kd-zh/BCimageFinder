# https://upload.neopets.com/beauty/images/winners/Poysion-2017-09-29.gif

import datetime

# Starting date
start_date = datetime.date(2000, 11, 27)  # Year, Month, Day
today = datetime.date.today()

def add_week(date):
    return date + datetime.timedelta(days=7)

# Function to handle irregularities with BC dates
def adjust_date(date):
    adjustments = {
        datetime.date(2001, 1, 15): datetime.date(2001, 1, 8),
        datetime.date(2004, 3, 15): datetime.date(2004, 3, 8)
    }
    return adjustments.get(date, date)

# Loop through dates
current_date = start_date
while current_date <= today:
    print(current_date)

    # Adjust date if it's an irregular case
    current_date = adjust_date(current_date)

    # Move to the next week
    current_date = add_week(current_date)
