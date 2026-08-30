from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def landing_view(request):
    return render(request, 'landing.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_view, name='landing'),
    
    # App UI Views
    path('accounts/', include('accounts.urls')),
    path('onboarding/', include('learners.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('roadmap/', include('roadmap.urls')),
    path('skill-gaps/', include('recommendations.urls')),
    path('resources/', include('resources.urls')),
    path('projects/', include('projects.urls')),
    path('assessments/', include('assessments.urls')),
    path('ai-assistant/', include('ai_assistant.urls')),
    path('profile/', include('learners.profile_urls')),
    
    # Django REST Framework API Endpoints
    path('api/', include([
        path('auth/', include('accounts.api_urls')),
        path('profile/', include('learners.api_urls')),
        path('roadmap/', include('roadmap.api_urls')),
        path('skill-gaps/', include('recommendations.api_urls')),
        path('resources/', include('resources.api_urls')),
        path('projects/', include('projects.api_urls')),
        path('dashboard/', include('dashboard.api_urls')),
        path('assessment/', include('assessments.api_urls')),
        path('ai/', include('ai_assistant.api_urls')),
    ])),
]
