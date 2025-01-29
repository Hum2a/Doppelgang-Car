from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify
from flask_cors import CORS
from deepface import DeepFace
import redis
import requests
import os
import re
import traceback
import random
import tensorflow as tf
import gc
import cv2

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

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

CAR_DATABASE = [
    {"make": "Ferrari", "model": "488 GTB", "year": 2022, "age_range": (18, 30), "emotion": ["happy", "excited"], "gender": "Man", "car_type": "Sports"},
    {"make": "Lamborghini", "model": "Huracan", "year": 2021, "age_range": (20, 35), "emotion": ["excited"], "gender": "Man", "car_type": "Supercar"},
    {"make": "Tesla", "model": "Model S", "year": 2023, "age_range": (25, 50), "emotion": ["neutral", "happy"], "gender": "Neutral", "car_type": "EV"},
    {"make": "Mercedes-Benz", "model": "E-Class", "year": 2020, "age_range": (30, 60), "emotion": ["neutral"], "gender": "Neutral", "car_type": "Luxury"},
    {"make": "Ford", "model": "F-150", "year": 2023, "age_range": (25, 60), "emotion": ["confident"], "gender": "Man", "car_type": "Truck"},
    {"make": "Volkswagen", "model": "Beetle", "year": 2021, "age_range": (18, 40), "emotion": ["happy", "calm"], "gender": "Woman", "car_type": "Hatchback"},
    {"make": "Jeep", "model": "Wrangler", "year": 2022, "age_range": (20, 50), "emotion": ["adventurous"], "gender": "Neutral", "car_type": "SUV"},
    {"make": "Toyota", "model": "Corolla", "year": 2020, "age_range": (18, 60), "emotion": ["neutral"], "gender": "Neutral", "car_type": "Sedan"},
]


def fetch_car_data(make, model, year):
    """Fetch car data from API Ninjas Cars API."""
    headers = {"X-Api-Key": API_KEY}
    params = {"make": make, "model": model, "year": year}
    
    try:
        print(f"[INFO] Fetching car data for: Make={make}, Model={model}, Year={year}")
        response = requests.get(BASE_URL, headers=headers, params=params)
        response.raise_for_status()
        car_data = response.json()
        print(f"[INFO] API Response: {car_data}")

        if isinstance(car_data, list) and len(car_data) > 0:
            return car_data[0]  # Return first match

        # **Fallback car if API returns no match**
        print("[WARNING] No car found, returning default car")
        return {
            "make": make,
            "model": model,
            "year": year,
            "error": "Exact match not found, using fallback values"
        }
    
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Error fetching car data: {e}")
        return {
            "make": "Unknown",
            "model": "Unknown",
            "year": "Unknown",
            "error": "Failed to fetch car data"
        }
    
def fetch_car_image(make, model):
    """Fetch a car image URL from Unsplash API."""
    UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"  # Replace with your Unsplash API Key
    search_query = f"{make} {model} car"
    url = f"https://api.unsplash.com/search/photos?query={search_query}&client_id={UNSPLASH_ACCESS_KEY}&per_page=1"

    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if "results" in data and len(data["results"]) > 0:
            return data["results"][0]["urls"]["regular"]  # Return the image URL
    except Exception as e:
        print(f"[ERROR] Could not fetch image for {make} {model}: {e}")

    return "https://via.placeholder.com/600x400.png?text=No+Image+Available"  # Default placeholder image


def analyze_image(image_path):
    """Analyze image to extract facial features."""
    try:
        print(f"[INFO] Processing image: {image_path}")

        # Resize image before analysis (reduce to 256x256 for efficiency)
        img = cv2.imread(image_path)
        img = cv2.resize(img, (256, 256))
        cv2.imwrite(image_path, img)  # Overwrite with smaller image

        # Analyze the image using default models for age, gender, and emotion
        results = DeepFace.analyze(
            img_path=image_path,
            actions=['age', 'gender', 'emotion']  # Actions determine which models are used
        )

        print(f"[INFO] Facial Analysis Result: {results}")

        if isinstance(results, list) and len(results) > 0:
            return results[0]  # Extract first detected face's attributes
        return None
    except Exception as e:
        print(f"[ERROR] DeepFace Analysis Failed: {e}")
        return None



def advanced_match_car(age, gender, emotion):
    """Finds the best car match using weighted decision making."""
    best_matches = []

    print(f"[INFO] Matching user: Age={age}, Gender={gender}, Emotion={emotion}")

    for car in CAR_DATABASE:
        age_min, age_max = car["age_range"]

        # Check if the age is in range
        age_match = age_min <= age <= age_max

        # Check if the emotion matches or is close
        emotion_match = emotion in car["emotion"]

        # Gender match (Neutral means it can match anyone)
        gender_match = (car["gender"] == "Neutral") or (car["gender"] == gender)

        # Assign score
        score = 0
        if age_match:
            score += 3  # Strong weight for age
        if emotion_match:
            score += 2  # Medium weight for emotion
        if gender_match:
            score += 1  # Lower weight for gender

        # If the car has a decent score, add it to possible matches
        if score > 3:
            best_matches.append((car, score))

    if best_matches:
        best_matches.sort(key=lambda x: x[1], reverse=True)  # Sort by highest score
        best_car = best_matches[0][0]  # Choose the best match
    else:
        print("[WARNING] No perfect match found, using fallback")
        best_car = random.choice(CAR_DATABASE)  # Choose a random fallback

    print(f"[INFO] Matched Car: {best_car}")
    return best_car["make"], best_car["model"], best_car["year"]


def map_features_to_car(age, gender, emotion):
    """Map facial attributes to car make, model, and year."""
    print(f"[INFO] Mapping features - Age: {age}, Gender: {gender}, Emotion: {emotion}")
    if age < 25:
        if gender == "Man":
            return "Ford", "Mustang", 2022
        else:
            return "Volkswagen", "Beetle", 2021
    elif age < 40:
        if emotion == "happy":
            return "Tesla", "Model 3", 2023
        else:
            return "BMW", "3 Series", 2020
    else:
        if emotion == "neutral":
            return "Mercedes-Benz", "E-Class", 2019
        else:
            return "Toyota", "Camry", 2018


@app.route('/process-photo', methods=['POST'])
def process_photo():
    print("[INFO] Received /process-photo request")

    if 'file' not in request.files:
        print("[ERROR] No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(file.filename))
    file.save(file_path)

    print(f"[INFO] File saved at: {file_path}")

    # Threaded processing
    with ThreadPoolExecutor() as executor:
        # Analyze the image
        future_analysis = executor.submit(analyze_image, file_path)
        features = future_analysis.result()

        if not features:
            print("[ERROR] No face detected or analysis failed")
            return jsonify({"error": "Facial analysis failed or no faces detected"}), 500

        # Extract data from features
        age = features.get('age', 30)
        gender = features.get('dominant_gender', "Man")
        emotion = features.get('dominant_emotion', "neutral")

        print(f"[INFO] Extracted features - Age: {age}, Gender: {gender}, Emotion: {emotion}")

        # Free memory related to features
        del features  # Delete the features variable to release memory
        gc.collect()  # Force garbage collection to release unused memory

        # Map features to a car
        make, model, year = advanced_match_car(age, gender, emotion)

        # Fetch car data
        future_car_data = executor.submit(fetch_car_data, make, model, year)
        car_data = future_car_data.result()

        # Fetch car image
        image_url = fetch_car_image(make, model)

        if car_data:
            car_data["image_url"] = image_url  # Add image URL to response

    print(f"[INFO] Final Car Match: {car_data}")
    return jsonify({"car": car_data})


def secure_filename(filename):
    """Sanitize the filename to ensure it's safe for use on any file system."""
    filename = re.sub(r'[^\w\s.-]', '', filename)
    filename = filename.replace(' ', '_')
    return filename or 'default_filename'

if __name__ == '__main__':
    print("[INFO] Starting Flask server...")
    app.run(debug=True)
