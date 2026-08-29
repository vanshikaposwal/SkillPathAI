from django.urls import path
from . import views

urlpatterns = [
    path('', views.assessment_list_view, name='assessments'),
    path('<int:pk>/', views.assessment_take_view, name='assessment_take'),
]
