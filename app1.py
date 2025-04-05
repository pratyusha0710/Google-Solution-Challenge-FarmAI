from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
from werkzeug.utils import secure_filename
import requests  # For API calls
from datetime import datetime

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Weather API configuration (using OpenWeatherMap as example)
WEATHER_API_KEY = '345b9292a4801ce824850a0eaeaf3e9d'  # Sign up at openweathermap.org for free API key
WEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/weather'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # Get weather data (example for New Delhi)
    weather_data = get_weather_data('New Delhi')
    return render_template('index.html', weather_data=weather_data)

@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Here you would call your AI model to analyze the image
        # For now, we'll return mock data
        analysis_results = analyze_image(filepath)  # Replace with actual model call
        
        return jsonify({
            'status': 'success',
            'image_url': f'static/uploads/{filename}',
            'results': analysis_results
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

def analyze_image(image_path):
    """Mock function to simulate AI analysis - replace with actual model calls"""
    # This is where you would integrate your crop disease detection model
    # For now, returning mock data
    
    return {
        'health_status': 'Healthy',
        'disease_detected': 'None',
        'confidence': '98%',
        'recommendations': 'Your crop appears healthy. Continue current care regimen.'
    }

def get_weather_data(location):
    """Fetch weather data from OpenWeatherMap API"""
    try:
        params = {
            'q': location,
            'appid': WEATHER_API_KEY,
            'units': 'metric'
        }
        response = requests.get(WEATHER_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        
        return {
            'temperature': data['main']['temp'],
            'description': data['weather'][0]['description'].capitalize(),
            'humidity': data['main']['humidity'],
            'wind_speed': data['wind']['speed'],
            'icon': data['weather'][0]['icon']
        }
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)