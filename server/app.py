from flask import Flask, request, jsonify
from flask_cors import CORS
import redis
import requests
import os

app = Flask(__name__)
CORS(app)

# Initialize Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# API Ninjas Cars API key
API_KEY = "ZxumjjS1ID9tk21k34zCZQ==AlUzWWFvPEaruyWL"
BASE_URL = "https://api.api-ninjas.com/v1/cars"

# Upload folder configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create the folder if it doesn't exist

def fetch_car_data(make, model, year):
    """Fetch car data from API Ninjas Cars API."""
    headers = {"X-Api-Key": API_KEY}
    params = {
        "make": make,
        "model": model,
        "year": year
    }
    try:
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        return response.json()  # Return car data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching car data: {e}")
        return None

@app.route('/process-photo', methods=['POST'])
def process_photo():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    # Save the file temporarily and process it
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Placeholder: Extract facial features and determine car attributes
    # Replace this with real facial recognition logic
    make = "Toyota"  # Replace with actual logic
    model = "Corolla"  # Replace with actual logic
    year = 2020  # Replace with actual logic

    # Fetch car data
    car_data = fetch_car_data(make, model, year)
    if car_data:
        return jsonify({"car": car_data})
    else:
        return jsonify({"error": "Could not fetch car data"}), 500

if __name__ == '__main__':
    app.run(debug=True)
