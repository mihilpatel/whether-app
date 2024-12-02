 
from flask import Flask, render_template, request
import requests
from datetime import datetime

app = Flask(__name__)

API_KEY = 'df054334246054f6f982b98c6ca8cc79'  # Replace with your OpenWeather API key

@app.template_filter('todate')
def todate(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%d %B %Y')
@app.template_filter('icon')
def icon(weather_condition):
    icon_map = {
        'Clear': 'wb_sunny',
        'Clouds': 'wb_cloudy',
        'Rain': 'umbrella',
        'Thunderstorm': 'flash_on',
        'Drizzle': 'grain',
        'Snow': 'ac_unit',
        'Mist': 'cloud',
        'Smoke': 'cloud',
        'Haze': 'cloud',
        'Fog': 'cloud',
    }
    return icon_map.get(weather_condition, 'help')  # Default to 'help' if no match found

@app.route('/', methods=['GET', 'POST'])
def home():
    weather_data = None
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            weather_data = fetch_weather_data(city)
            if not weather_data:
                error_message = "City not found or unable to fetch data."

    return render_template('index.html', weather=weather_data, error=error_message)

def fetch_weather_data(city):
    try:
        response = requests.get(
            f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}'
        )
        print(f"Response URL: {response.url}")
        if response.ok:
            return response.json()
        else:
            print(f"Error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
