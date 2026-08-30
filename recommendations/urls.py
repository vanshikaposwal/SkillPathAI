from django.urls import path
from . import views
urlpatterns = [
    path('', views.skill_gaps_view, name='skill_gaps'),
]
