import requests
from datetime import datetime
import pytz

# Function to get the user's IP address location (you can use an external service)
def get_location():
    try:
        # Trying to access the IP-based location service without timeout
        response = requests.get('https://ipinfo.io')
        response.raise_for_status()  # Raises HTTPError for bad responses (4xx, 5xx)
        data = response.json()
        location = data.get('city', 'Unknown') + ", " + data.get('region', 'Unknown') + ", " + data.get('country', 'Unknown')
        return location, data.get('timezone', 'UTC')
    except (requests.exceptions.RequestException, requests.exceptions.ConnectionError) as e:
        # Handle error if there's no internet or an issue with the request
        return None, None

def get_current_time(timezone_str):
    # Get timezone using pytz
    timezone = pytz.timezone(timezone_str)
    # Get the current time in the given timezone
    local_time = datetime.now(timezone)
    return local_time.strftime('%A, %Y-%m-%d %H:%M:%S')  # %A for the day of the week

def get_time_based_on_location():
    # Try to get location information
    location, timezone_str = get_location()

    if location is not None and timezone_str is not None:
        # Return location, timezone, and the current time
        current_time = get_current_time(timezone_str)
        return location, timezone_str, current_time
    else:
        # If no internet, fallback to Singapore Time (SGT)
        timezone_str = "Asia/Singapore"  # Singapore Time (SGT) timezone
        current_time = get_current_time(timezone_str)
        return "Unable to fetch location. Falling back to Singapore Time (SGT).", timezone_str, current_time

while True:
    # Example usage
    location, timezone, current_time = get_time_based_on_location()

    # You can now use these variables as needed
    print(location)       # Location: San Francisco, CA, US or "Unknown location"
    print(timezone)       # Timezone: America/Los_Angeles or Asia/Singapore
    print(current_time)   # Current time in the respective timezone

