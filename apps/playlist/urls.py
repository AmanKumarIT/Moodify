from django.urls import path
from .views import generate_playlist, get_history

urlpatterns = [
    path('generate/', generate_playlist, name='generate_playlist'),
    path('history/', get_history, name='get_history'),
]
