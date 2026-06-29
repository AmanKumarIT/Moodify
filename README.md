
<p align="center">
  <h1 align="center">Moodify Backend</h1>
  <p align="center">
    AI Emotion Detection & Playlist Recommendation API
  </p>
</p>

---

## 📖 Overview

This repository contains the backend services for **Moodify**, responsible for emotion detection, AI model inference, playlist recommendation logic, and communication with the frontend.

The backend processes uploaded images, predicts the user's emotion using a trained machine learning model, and returns matching Spotify playlists.

---

## ✨ Features

* 🤖 AI Emotion Detection
* 📷 Image Processing
* 🎵 Playlist Recommendation API
* 🔐 RESTful API
* ⚡ Fast Prediction Pipeline
* 📊 JSON Responses
* 🧠 Machine Learning Integration

---

## 🛠 Tech Stack

* Python
* Flask
* OpenCV
* NumPy
* TensorFlow / Keras
* scikit-learn
* Pillow

---

## 📂 Project Structure

```text
backend/
│
├── app.py
├── model/
│   ├── emotion_model.pkl
│   ├── label_encoder.pkl
│
├── routes/
├── services/
├── utils/
├── uploads/
├── requirements.txt
└── README.md
```

---

## ⚙️ Environment Variables

Create a `.env` file.

```env
PORT=5000
FLASK_ENV=development
MODEL_PATH=model/emotion_model.pkl
LABEL_ENCODER_PATH=model/label_encoder.pkl
```

---

## 🚀 Installation

Clone repository

```bash
git clone https://github.com/yourusername/moodify-backend.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run server

```bash
python app.py
```

---

## 📡 API Endpoints

### Detect Mood

```http
POST /api/mood/detect
```

Request

```json
{
  "image": "<uploaded-image>"
}
```

Response

```json
{
  "success": true,
  "emotion": "Happy",
  "confidence": 0.97,
  "playlists": [
    {
      "name": "Happy Hits",
      "url": "https://spotify.com/..."
    }
  ]
}
```

---

## 🧠 Machine Learning Pipeline

```text
Receive Image
      │
      ▼
Image Preprocessing
      │
      ▼
Face Detection
      │
      ▼
Feature Extraction
      │
      ▼
Emotion Prediction
      │
      ▼
Playlist Recommendation
      │
      ▼
JSON Response
```

---

## 🎵 Supported Emotions

* Happy
* Sad
* Angry
* Neutral
* Fear
* Surprise
* Disgust

---

## 📦 Dependencies

* Flask
* OpenCV
* NumPy
* Pillow
* TensorFlow
* scikit-learn
* Flask-CORS

Install

```bash
pip install -r requirements.txt
```

---

## 🧪 Testing

Run backend

```bash
python manage.py runserver
```

Test endpoint using Postman

```http
POST http://localhost:5000/api/mood/detect
```

---

## 🔒 Security

* Image Validation
* File Size Validation
* CORS Configuration
* Temporary File Cleanup
* Error Handling

---

## 📄 License


## 👨‍💻 Author

Developed as part of the **Moodify** AI Playlist Recommendation System.
