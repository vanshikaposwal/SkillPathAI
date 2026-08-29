from django.urls import path
from . import views

urlpatterns = [
    path('', views.roadmap_view, name='roadmap'),
    path('<int:pk>/', views.roadmap_detail_view, name='roadmap_detail'),
]
