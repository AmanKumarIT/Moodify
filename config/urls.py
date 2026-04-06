from django.urls import path, include
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    path('api/health/', health_check),
    path('api/auth/', include('apps.custom_auth.urls')),
    path('api/emotion/', include('apps.emotion.urls')),
    path('api/playlist/', include('apps.playlist.urls')),
]
