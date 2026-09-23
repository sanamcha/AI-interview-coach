import json
import ssl
from urllib.parse import urlencode
from urllib.request import urlopen
from urllib.error import URLError
import certifi
from flask import Flask, render_template, request
app = Flask(__name__)
DESCRIPTIONS = {0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy', 3: 'Overcast', 45: 'Fog', 48: 'Rime fog', 51: 'Light drizzle', 53: 'Drizzle', 55: 'Heavy drizzle', 56: 'Freezing drizzle', 57: 'Heavy freezing drizzle', 61: 'Light rain', 63: 'Rain', 65: 'Heavy rain', 66: 'Freezing rain', 67: 'Heavy freezing rain', 71: 'Light snow', 73: 'Snow', 75: 'Heavy snow', 77: 'Snow grains', 80: 'Light showers', 81: 'Showers', 82: 'Heavy showers', 85: 'Snow showers', 86: 'Heavy snow showers', 95: 'Thunderstorm', 96: 'Thunderstorm with hail', 99: 'Thunderstorm with heavy hail'}

def get_json(url):
    with urlopen(url, timeout=15, context=ssl.create_default_context(cafile=certifi.where())) as response:
        return json.load(response)

def display(value, unit):
    return 'Unavailable' if value is None else f'{value} {unit}'

@app.get('/')
def index():
    city = request.args.get('city', '').strip()
    result, error = None, None
    if 'city' in request.args:
        if not city or len(city) > 100:
            error = 'Enter a city name (1–100 characters).'
        else:
            try:
                geo = get_json('https://geocoding-api.open-meteo.com/v1/search?' + urlencode({'name':city,'count':1,'language':'en'}))
                places = geo.get('results', [])
                if not places:
                    error = 'City not found. Check the spelling and try again.'
                else:
                    place = places[0]
                    data = get_json('https://api.open-meteo.com/v1/forecast?' + urlencode({'latitude':place['latitude'],'longitude':place['longitude'],'current':'temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m','timezone':'auto'}))
                    current = data.get('current', {})
                    if current.get('temperature_2m') is None:
                        error = 'Current weather is unavailable for this city.'
                    else:
                        result = {'place': ', '.join(str(place[k]) for k in ('name','admin1','country') if place.get(k)), 'current':current,'timezone':data.get('timezone','Local time'),'description':DESCRIPTIONS.get(current.get('weather_code'),'Unknown conditions')}
            except (URLError, TimeoutError, ValueError, KeyError, TypeError):
                error = 'Weather service unavailable. Please try again.'
    return render_template('index.html', city=city, result=result, error=error, display=display)

if __name__ == '__main__':
    app.run(port=5001)
