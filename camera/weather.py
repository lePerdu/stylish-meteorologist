"""Weather fetching.
This currently uses the city ID from the .env file, but should in the future
fetch its current city ID / geographic coordinates.
"""

import os

import requests

TEMPERATURE_UNITS = os.environ['TEMPERATURE_UNITS']
OPENWEATHERMAP_API_KEY = os.environ['OPENWEATHERMAP_API_KEY']


class Weather:
    def __init__(self, temp, min_temp, max_temp, is_raining):
        self.cur_temp = temp
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.is_raining = is_raining


def get_weather():
    zip_code = get_zip_code()
    resp = requests.get(
        'https://api.openweathermap.org/data/2.5/weather',
        params={
            'zip': zip_code,
            'units': TEMPERATURE_UNITS,
            'appid': OPENWEATHERMAP_API_KEY,
        })

    data = resp.json()

    temp = data['main']['feels_like']
    min_temp, max_temp = data['main']['temp_min'], data['main']['temp_max']
    # Multiple weather conditions are sent
    raining = any(w['main'] == "Rain" for w in data['weather'])

    return Weather(temp, min_temp, max_temp, raining)


def get_zip_code():
    """Use ip-api.com to geolocate current IP address."""
    data = requests.get('http://ip-api.com/json').json()
    return data['zip']
