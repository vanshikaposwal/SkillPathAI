from django.urls import path
from . import views

urlpatterns = [
    path('', views.onboarding_start, name='onboarding_start'),
    path('step/<int:step>/', views.onboarding_step_view, name='onboarding_step'),
]
