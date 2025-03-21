# DoppelGang-Car

A fun web application that analyzes your facial features and determines which car you resemble most.

## 📝 Project Overview

DoppelGang-Car uses AI-powered facial recognition to analyze your photos and match your features to a car that best represents your personality. The application consists of:

- **Frontend**: Nuxt.js web application with responsive design
- **Backend**: Flask REST API with facial analysis capabilities
- **AI Engine**: Utilizes DeepFace framework for facial attribute extraction

## 🛠️ Technology Stack

### Frontend
- **Framework**: Nuxt.js 3.x / Vue.js
- **Styling**: CSS with custom styling
- **HTTP Client**: Native fetch API

### Backend
- **Framework**: Flask (Python)
- **Facial Analysis**: DeepFace
- **Image Processing**: OpenCV
- **API Integration**: API Ninjas Cars API

## 🚀 Setup Instructions

### Prerequisites
- Node.js (v16+)
- Python (v3.8+)
- Redis (optional, for caching)

### Environment Variables Setup

1. For the backend, create or modify the `.env` file in the `server` directory:
```
API_KEY=your_api_ninjas_key
BASE_URL=https://api.api-ninjas.com/v1/cars
UNSPLASH_ACCESS_KEY=your_unsplash_api_key
```

You'll need to sign up for free API keys at:
- [API Ninjas](https://api-ninjas.com/api/cars) for car data
- [Unsplash API](https://unsplash.com/developers) for car images (optional)

2. For the frontend, create a `.env` file in the `client` directory if additional environment variables are needed.

### Backend Setup

1. Navigate to the server directory:
```bash
cd server
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
python app.py
```
The server will start at http://127.0.0.1:5000

### Frontend Setup

1. Navigate to the client directory:
```bash
cd client
```

2. Install dependencies:
```bash
npm install
```

3. Run the development server:
```bash
npm run dev
```
The application will be available at http://localhost:3000

## 📋 How It Works

1. Upload a photo containing your face
2. The backend processes the image using DeepFace to extract facial attributes:
   - Age
   - Gender
   - Dominant emotion
3. These attributes are mapped to car characteristics
4. The application matches you with a car that best represents you
5. Details about the matched car are displayed on the screen

## 🚀 Deployment

### Local Development
- Frontend: Runs on http://localhost:3000
- Backend: Runs on http://localhost:5000

### Cloud Deployment
When deploying to cloud platforms like Render, Heroku, or AWS:

1. The backend automatically binds to `0.0.0.0` and uses the `PORT` environment variable provided by the platform
2. Make sure to set all required environment variables on your deployment platform:
   - `API_KEY` - Your API Ninjas key
   - `UNSPLASH_ACCESS_KEY` - Your Unsplash API key (optional)
   - Any other configuration variables your deployment requires

3. For the frontend, update the API endpoint URL to point to your deployed backend:
   ```
   NUXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

### Troubleshooting Deployment
- Ensure all environment variables are properly set
- Check that the application is binding to the correct host and port
- Verify that CORS is properly configured for your production domains

## 🔍 API Endpoints

### POST /process-photo
Processes an uploaded photo and returns car match information.

**Request Body:**
- `file`: The image file to be processed (multipart/form-data)

**Response:**
```json
{
  "car": {
    "make": "Tesla",
    "model": "Model 3",
    "year": 2023,
    "image_url": "https://example.com/car-image.jpg"
  }
}
```

## 🧩 Project Structure

```
project-root/
├── client/               # Frontend Nuxt.js application
│   ├── components/       # Reusable Vue components
│   ├── layouts/          # Page layouts
│   ├── pages/            # Application pages
│   ├── public/           # Static assets
│   └── styles/           # Global CSS styles
│
├── server/               # Backend Flask application
│   ├── app.py            # Main application file
│   ├── requirements.txt  # Python dependencies
│   └── uploads/          # Directory for uploaded images
```

## 🔒 Privacy Notice

All uploaded photos are processed locally and are not permanently stored. Images are temporarily saved for processing and are removed after analysis is complete.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Contributors

- [Your Name] - Initial work 