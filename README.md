# Weather Information App (REST API Project)

A beginner-friendly Python application that connects to the
[OpenWeatherMap](https://openweathermap.org/api) REST API, parses the JSON
response, stores it in a custom class using OOP, and prints a formatted
weather summary.

## Features

- Sends an HTTP GET request to the OpenWeatherMap *Current Weather* API
- Parses the JSON response and extracts: city, country, temperature,
  feels-like temperature, weather description, humidity and wind speed
- Stores the data in a `WeatherData` class with a `display_summary()` method
- Reads the API key from a `.env` file (never hard-coded)
- Handles errors gracefully: missing API key, invalid city, connection
  errors, timeouts, HTTP errors, invalid JSON and missing fields

## Project Structure

```
REST_API_Project/
├── main.py            # the application
├── requirements.txt   # Python dependencies
├── .env.example       # template for the API key file
├── .gitignore         # keeps .env and venv/ out of Git
└── README.md
```

## Requirements

- Python 3.8 or newer
- A free OpenWeatherMap API key: https://home.openweathermap.org/api_keys
  (new keys can take up to a couple of hours to activate)

## Setup (Windows)

```bat
:: 1. Create the virtual environment
python -m venv venv

:: 2. Activate it
venv\Scripts\activate            :: Command Prompt
venv\Scripts\Activate.ps1        :: PowerShell

:: 3. Install the dependencies
pip install -r requirements.txt
```

If PowerShell blocks the activation script, run
`Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` first.

### Create the `.env` file

Copy `.env.example` to a new file named `.env` and put your real key in it:

```
API_KEY=your_real_api_key_here
```

> `.env` is listed in `.gitignore`, so your key is never uploaded to GitHub.

## Run

```bat
python main.py
```

Enter a city name when asked. Example output (illustrative values):

```
========================================
          WEATHER INFORMATION
========================================

City           : Cairo
Country        : EG
Temperature    : 25.0°C
Feels Like     : 27.0°C
Weather        : Clear Sky
Humidity       : 45%
Wind Speed     : 3.5 m/s

========================================
```

## How It Works

1. `get_api_key()` loads the key from `.env` using `python-dotenv`.
2. `ask_city_name()` asks for a city and rejects empty input.
3. `fetch_weather_json()` sends the GET request and returns the parsed JSON.
4. `parse_weather_data()` extracts the needed fields and creates a
   `WeatherData` object.
5. `WeatherData.display_summary()` prints the formatted result.

All expected problems are raised as `WeatherError` and shown to the user as a
readable message instead of a crash.

## Security

- The API key is stored only in `.env` (ignored by Git).
- `.env.example` contains a placeholder, never a real key.

## Technologies

Python · `requests` · `python-dotenv` · OpenWeatherMap API
