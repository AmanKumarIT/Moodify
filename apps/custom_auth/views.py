import json
import bcrypt
import jwt
from datetime import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from utils.db import db
from django.conf import settings

SECRET_KEY = settings.SECRET_KEY

@csrf_exempt
def register_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        data = json.loads(request.body)
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if not username or not email or not password:
            return JsonResponse({"error": "Missing required fields"}, status=400)
        
        # Check if user exists
        if db.users.find_one({"email": email}) or db.users.find_one({"username": username}):
            return JsonResponse({"error": "User already exists"}, status=400)

        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        user_id = db.users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password
        }).inserted_id

        return JsonResponse({"message": "User registered successfully", "user_id": str(user_id)}, status=201)
    
    except Exception as e:
        import traceback
        print(f"ERROR in register_view: {e}")
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def login_view(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    
    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"error": "Missing required fields"}, status=400)

        user = db.users.find_one({"email": email})
        if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"]):
            return JsonResponse({"error": "Invalid credentials"}, status=401)
        
        # Generate JWT with integer expiration
        exp_time = int(datetime.datetime.utcnow().timestamp()) + 86400
        
        token = jwt.encode({
            "user_id": str(user["_id"]),
            "username": user["username"],
            "exp": exp_time
        }, SECRET_KEY, algorithm="HS256")

        # PyJWT 1.x returns bytes, PyJWT 2.x returns str
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return JsonResponse({
            "message": "Login successful",
            "token": token,
            "username": user["username"],
            "user_id": str(user["_id"])
        }, status=200)

    except Exception as e:
        import traceback
        print(f"ERROR in login_view: {e}")
        traceback.print_exc()
        return JsonResponse({"error": str(e)}, status=500)


def verify_token(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        # Silently fail for internal check, but log for debugging
        return None
        
    if not auth_header.startswith("Bearer "):
        print(f"DEBUG: Invalid header format: {auth_header[:15]}...")
        return None
    
    parts = auth_header.split(" ")
    if len(parts) != 2:
        print("DEBUG: Authorization header split error")
        return None
        
    token = parts[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        print("DEBUG: Token Expired")
        return None
    except jwt.InvalidTokenError as e:
        print(f"DEBUG: Invalid Token: {e}")
        return None
    except Exception as e:
        print(f"DEBUG: Unexpected Token Error: {e}")
        return None

@csrf_exempt
def me_view(request):
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)
        
    payload = verify_token(request)
    if not payload:
        return JsonResponse({"error": "Unauthorized"}, status=401)
        
    return JsonResponse({"user": payload}, status=200)

def health_check(request):
    return JsonResponse({
        "status": "ok",
        "time": datetime.utcnow().isoformat()
    })