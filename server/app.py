from flask import Flask, request, jsonify
from flask_cors import CORS
import redis

app = Flask(__name__)
CORS(app)

# Initialize Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

@app.route('/process-photo', methods=['POST'])
def process_photo():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    # Save the file temporarily and process it
    file_path = f"uploads/{file.filename}"
    file.save(file_path)

    # Perform facial recognition and suggest a car (placeholder logic)
    car_suggestion = "Toyota Corolla"  # Replace with actual logic
    return jsonify({"car": car_suggestion})

if __name__ == '__main__':
    app.run(debug=True)
