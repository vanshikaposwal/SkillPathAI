from django.urls import path
from . import views

urlpatterns = [
    path('', views.assistant_view, name='ai_assistant'),
    path('clear/', views.clear_history_view, name='clear_ai_history'),
]
