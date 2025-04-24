from flask import Flask, request, redirect, url_for, render_template, flash
import pickle
import os
import requests

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()

# Load trained model pipeline
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

API_KEY = "930c05cd5069d54bc6c6e69e945f83d6"
WEATHERSTACK_URL = "http://api.weatherstack.com/current"

def get_weather_data(place):
    """Fetch weather data from Weatherstack for a given location"""
    params = {
        'access_key': API_KEY,
        'query': place
    }

    try:
        response = requests.get(WEATHERSTACK_URL, params=params, timeout=10)

        # Handle unauthorized access
        if response.status_code == 401:
            return None, "⚠ API key is unauthorized. Please contact the developer."

        response.raise_for_status()
        data = response.json()

        if "error" in data:
            return None, f"❌ {data['error'].get('info', 'Location not found or API error.')}"

        current = data.get("current", {})
        return {
            'temp': current.get('temperature', 25.0),
            'humidity': current.get('humidity', 50),
            'wind_speed': current.get('wind_speed', 2.0),
            'precipitation': current.get('precip', 0.0)
        }, None

    except requests.exceptions.RequestException:
        return None, "⚠ Network error: Please check your internet connection."
    except Exception as e:
        return None, f"⚠ Unexpected error: {str(e)}"

@app.route('/')
def home():
    return render_template("forest_fire.html")

@app.route('/predict', methods=['POST'])
def predict():
    place = request.form.get('Place', '').strip()

    if not place:
        flash('⚠ Please enter a valid location name.', 'error')
        return redirect(url_for('home'))

    weather_data, error = get_weather_data(place)
    if error:
        flash(error, 'error')
        return redirect(url_for('home'))

    try:
        features = [[
            weather_data['temp'],
            weather_data['humidity'],
            weather_data['wind_speed'],
            weather_data['precipitation']
        ]]

        # Predict fire probability
        proba = model.predict_proba(features)[0][1] * 100
        output = f'{proba:.1f}%'

        # Alert levels
        if proba > 75:
            alert_type = 'danger'
            message = f'🔥 High Fire Risk! ({output})'
            advice = 'Evacuation recommended - contact authorities immediately'
        elif proba > 50:
            alert_type = 'warning'
            message = f'⚠ Moderate Fire Risk ({output})'
            advice = 'Heightened alert - monitor conditions closely'
        else:
            alert_type = 'success'
            message = f'✅ Low Fire Risk ({output})'
            advice = 'Normal precautions advised'

        # Show messages
        flash(message, alert_type)
        flash(advice, 'advice')
        flash(f'Current Weather: {weather_data["temp"]}°C, '
              f'{weather_data["humidity"]}% Humidity, '
              f'{weather_data["wind_speed"]} km/h Wind, '
              f'{weather_data["precipitation"]} mm Rain', 'conditions')

    except Exception as e:
        flash(f'⚠ Prediction Error: {str(e)}', 'error')

    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
