import os
import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.db import db
from apps.custom_auth.views import verify_token
from googleapiclient.discovery import build
import random

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

EMOTION_KEYWORDS = {
    "happy": ["upbeat pop", "happy indie", "feel good songs"],
    "sad": ["melancholy indie", "sad acoustic", "heartbreak songs"],
    "angry": ["metalcore", "hard rock", "aggressive rap"],
    "neutral": ["lofi hip hop", "chillwave", "ambient study"],
    "surprise": ["electronic dance music", "hyperpop", "synthwave"]
}

@csrf_exempt
def generate_playlist(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    payload = verify_token(request)
    
    try:
        data = json.loads(request.body)
        emotion = data.get("emotion")
        
        if not emotion:
            return JsonResponse({"error": "Emotion is required"}, status=400)
            
        emotion = emotion.lower()
        if emotion not in EMOTION_KEYWORDS:
            emotion = "neutral"
            
        queries = EMOTION_KEYWORDS.get(emotion)
        query = random.choice(queries)
        
        songs = []
        if YOUTUBE_API_KEY:
            youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
            req = youtube.search().list(
                q=query,
                part='snippet',
                type='video',
                maxResults=5,
                videoCategoryId='10' # Music
            )
            res = req.execute()
            for item in res.get('items', []):
                songs.append({
                    "title": item['snippet']['title'],
                    "youtube_url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    "videoId": item['id']['videoId'],
                    "thumbnail": item['snippet']['thumbnails']['high']['url']
                })
        else:
            # MOCK DATA
            songs = [
                {
                    "title": f"Mock Song for {emotion} ({i})",
                    "youtube_url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                    "videoId": "dQw4w9WgXcQ",
                    "thumbnail": "https://img.youtube.com/vi/dQw4w9WgXcQ/hqdefault.jpg"
                } for i in range(1, 6)
            ]
            
        playlist_id = None
        # Save to history if logged in
        if payload:
            user_id = payload.get("user_id")
            result = db.playlists.insert_one({
                "user_id": user_id,
                "emotion": emotion,
                "created_at": datetime.utcnow()
            })
            playlist_id = result.inserted_id
            
            for song in songs:
                song['playlist_id'] = str(playlist_id)
                db.songs.insert_one(song.copy())
                
        return JsonResponse({
            "emotion": emotion,
            "songs": songs,
            "playlist_id": str(playlist_id) if playlist_id else None
        }, status=200)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def get_history(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    payload = verify_token(request)
    if not payload:
        return JsonResponse({"error": "Unauthorized"}, status=401)
        
    user_id = payload.get("user_id")
    try:
        playlists_cursor = db.playlists.find({"user_id": user_id}).sort("created_at", -1)
        history = []
        
        for p in playlists_cursor:
            songs_cursor = db.songs.find({"playlist_id": str(p["_id"])})
            songs = []
            for s in songs_cursor:
                songs.append({
                    "title": s.get("title"),
                    "youtube_url": s.get("youtube_url"),
                    "thumbnail": s.get("thumbnail"),
                    "videoId": s.get("videoId")
                })
            history.append({
                "id": str(p["_id"]),
                "emotion": p.get("emotion"),
                "created_at": p.get("created_at").isoformat(),
                "songs": songs
            })
            
        return JsonResponse({"history": history}, status=200)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
