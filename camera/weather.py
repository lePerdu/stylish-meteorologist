"""Weather fetching.
This currently uses the city ID from the .env file, but should in the future
fetch its current city ID / geographic coordinates.
"""

import os

import requests

CITY_ID = os.environ['OPEN_WEATHER_CITY_ID']
TEMPERATURE_UNITS = os.environ['TEMPERATURE_UNITS']


class Weather:
    def __init__(self, temp, min_temp, max_temp, is_raining):
        self.cur_temp = temp
        self.min_temp = min_temp
        self.max_temp = max_temp
        self.is_raining = is_raining


def get_weather():
    resp = requests.get(
        'https://openweathermap.org/data/2.5/weather',
        params={
            'id': CITY_ID,
            'units': TEMPERATURE_UNITS,
        })

    data = resp.json()

    temp = data['main']['feels_like']
    min_temp, max_temp = data['main']['temp_min'], data['main']['temp_max']
    raining = data['weather']['main'] == "Rain"

    return Weather(temp, min_temp, max_temp, raining)
