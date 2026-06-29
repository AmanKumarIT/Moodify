
<p align="center">
  <h1 align="center">Moodify</h1>
  <p align="center">
    AI-Powered Mood-Based Playlist Generator Frontend
  </p>
</p>

---

## 📖 Overview

Moodify is an AI-powered web application that analyzes a user's facial expression to detect their current mood and automatically recommends personalized Spotify playlists.

This repository contains the **React frontend**, responsible for the user interface, webcam integration, mood visualization, playlist display, and communication with the backend API.

---

## ✨ Features

* 🎥 Webcam Integration
* 😊 Real-Time Mood Detection
* 🎵 Spotify Playlist Recommendations
* 📱 Responsive Design
* ⚡ Fast React UI
* 🔄 API Integration
* 🎨 Modern User Interface
* 🌙 Clean & Minimal Design

---

## 🛠 Tech Stack

* React.js
* Vite
* JavaScript
* Tailwind CSS
* Axios
* React Router DOM

---

## 📂 Project Structure

```text
src/
│
├── assets/
├── components/
├── pages/
├── hooks/
├── services/
├── utils/
├── App.jsx
├── main.jsx
└── index.css
```

---

## ⚙️ Environment Variables

Create a `.env` file.

```env
VITE_API_URL=http://localhost:5000/api
```

---

## 🚀 Installation

Clone the repository

```bash
git clone https://github.com/yourusername/moodify-frontend.git
```

Install dependencies

```bash
npm install
```

Run development server

```bash
npm run dev
```

---

## 📡 Backend Connection

The frontend communicates with the backend through REST APIs.

Example:

```text
POST /api/mood/detect
```

---

## 📱 Features Implemented

* Webcam Capture
* Mood Detection Interface
* Playlist Recommendation Page
* Loading Animations
* Error Handling
* API Integration

---

## 📸 Workflow

```text
User Opens Website
        │
        ▼
Allow Webcam Access
        │
        ▼
Capture Face Image
        │
        ▼
Send Image to Backend
        │
        ▼
Receive Mood Prediction
        │
        ▼
Display Spotify Playlists
```

---

## 📦 Build

Development

```bash
npm run dev
```

Production

```bash
npm run build
```

Preview

```bash
npm run preview
```

---

## 🤝 Contributing

1. Fork Repository
2. Create Feature Branch
3. Commit Changes
4. Push Changes
5. Open Pull Request

---

## 📄 License

MIT License

---

## 👨‍💻 Author

Developed as part of the **Moodify** AI Playlist Recommendation project.
