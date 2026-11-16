"""
Weather Information App
-----------------------
Asks the user for a city name, calls the OpenWeatherMap "Current Weather"
API, stores the result in a WeatherData object and prints a summary.
"""

import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
API_URL = "https://api.openweathermap.org/data/2.5/weather"
REQUEST_TIMEOUT = 10  # seconds to wait for the server before giving up
PLACEHOLDER_KEY = "YOUR_OPENWEATHERMAP_API_KEY"  # value used in .env.example
LINE_WIDTH = 40


# ---------------------------------------------------------------------------
# Custom exception: every problem we expect is raised as WeatherError, so
# main() can catch one exception type and show a friendly message.
# ---------------------------------------------------------------------------
class WeatherError(Exception):
    """A problem that should be explained to the user (not a crash)."""


# ---------------------------------------------------------------------------
# The class that stores the weather information (OOP part of the task)
# ---------------------------------------------------------------------------
class WeatherData:
    """Holds the weather information for one city."""

    def __init__(self, city, country, temperature, feels_like,
                 description, humidity, wind_speed):
        # Each value is stored as an attribute of the object.
        self.city = city
        self.country = country
        self.temperature = temperature    # degrees Celsius
        self.feels_like = feels_like      # degrees Celsius
        self.description = description    # e.g. "clear sky"
        self.humidity = humidity          # percent
        self.wind_speed = wind_speed      # metres per second

    def display_summary(self):
        """Print the weather information in a formatted layout."""
        line = "=" * LINE_WIDTH
        rows = [
            ("City", self.city),
            ("Country", self.country),
            ("Temperature", f"{self.temperature:.1f}°C"),
            ("Feels Like", f"{self.feels_like:.1f}°C"),
            ("Weather", self.description.title()),
            ("Humidity", f"{self.humidity}%"),
            ("Wind Speed", f"{self.wind_speed:.1f} m/s"),
        ]

        print(f"\n{line}")
        print("WEATHER INFORMATION".center(LINE_WIDTH))
        print(line)
        print()
        for label, value in rows:
            print(f"{label:<15}: {value}")   # label padded to 15 characters
        print(f"\n{line}")


# ---------------------------------------------------------------------------
# Step 1: read the API key from the .env file
# ---------------------------------------------------------------------------
def get_api_key():
    """Load the API key from .env (next to this file) and return it."""
    env_path = Path(__file__).resolve().parent / ".env"
    load_dotenv(dotenv_path=env_path)       # puts .env values into os.environ
    api_key = os.getenv("API_KEY", "").strip()

    if not api_key or api_key == PLACEHOLDER_KEY:
        raise WeatherError(
            "API key not found. Create a .env file next to main.py "
            "containing:  API_KEY=your_real_key"
        )
    return api_key


# ---------------------------------------------------------------------------
# Step 2: ask the user for a city name
# ---------------------------------------------------------------------------
def ask_city_name():
    """Keep asking until the user types something that is not empty."""
    while True:
        city = input("Enter a city name: ").strip()
        if city:
            return city
        print("The city name cannot be empty. Please try again.")


# ---------------------------------------------------------------------------
# Step 3: call the API and return the parsed JSON (a Python dictionary)
# ---------------------------------------------------------------------------
def fetch_weather_json(city, api_key):
    """Send the GET request and return the JSON response as a dict."""
    params = {
        "q": city,           # city name
        "appid": api_key,    # API key
        "units": "metric",   # Celsius and metres/second
    }

    try:
        response = requests.get(API_URL, params=params, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.Timeout:
        raise WeatherError("The request timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise WeatherError("Could not connect. Check your internet connection.")
    except requests.exceptions.RequestException as error:
        raise WeatherError(f"The request failed: {error}")

    # HTTP status codes: 200 = success, anything else = a problem.
    if response.status_code == 401:
        raise WeatherError("Invalid API key. New keys can take a while to activate.")
    if response.status_code == 404:
        raise WeatherError(f"City '{city}' was not found. Check the spelling.")
    if response.status_code == 429:
        raise WeatherError("Too many requests. Please wait a moment and retry.")
    try:
        response.raise_for_status()   # raises for any other 4xx / 5xx code
    except requests.exceptions.HTTPError:
        raise WeatherError(f"The server returned HTTP error {response.status_code}.")

    try:
        return response.json()        # JSON text -> Python dictionary
    except ValueError:
        raise WeatherError("The server sent an invalid JSON response.")


# ---------------------------------------------------------------------------
# Step 4: pull out the fields we need and build a WeatherData object
# ---------------------------------------------------------------------------
def parse_weather_data(data):
    """Convert the API's JSON dictionary into a WeatherData object."""
    try:
        return WeatherData(
            city=data["name"],
            country=data["sys"]["country"],
            temperature=float(data["main"]["temp"]),
            feels_like=float(data["main"]["feels_like"]),
            description=data["weather"][0]["description"],
            humidity=int(data["main"]["humidity"]),
            wind_speed=float(data["wind"]["speed"]),
        )
    except (KeyError, IndexError, TypeError, ValueError):
        raise WeatherError("The API response is missing expected weather fields.")


# ---------------------------------------------------------------------------
# Program entry point
# ---------------------------------------------------------------------------
def main():
    try:
        api_key = get_api_key()
        city = ask_city_name()
        data = fetch_weather_json(city, api_key)
        weather = parse_weather_data(data)   # create the object
        weather.display_summary()            # print the summary
    except WeatherError as error:
        print(f"\nError: {error}")
        sys.exit(1)
    except (KeyboardInterrupt, EOFError):
        print("\nCancelled.")
        sys.exit(0)


if __name__ == "__main__":
    main()
