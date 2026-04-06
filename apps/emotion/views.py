import json
import base64
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.db import db
from utils.model_loader import emotion_model
from apps.custom_auth.views import verify_token

@csrf_exempt
def predict_emotion(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    payload = verify_token(request)
    # We allow unauthenticated requests for testing, but ideally we want a user
    
    try:
        data = json.loads(request.body)
        image_base64 = data.get("image")
        
        if not image_base64:
            return JsonResponse({"error": "No image provided"}, status=400)
            
        prediction = emotion_model.predict(image_base64)
        
        if "error" in prediction:
            return JsonResponse({"error": prediction["error"]}, status=500)
            
        emotion = prediction.get("emotion")
        confidence = prediction.get("confidence")
        
        # Save to DB if authenticated
        if payload:
            user_id = payload.get("user_id")
            db.emotions.insert_one({
                "user_id": user_id,
                "emotion_type": emotion,
                "confidence": confidence,
                "timestamp": datetime.utcnow()
            })
            
        return JsonResponse(prediction, status=200)
        
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
