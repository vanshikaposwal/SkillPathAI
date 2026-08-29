from django.urls import path
from . import views

urlpatterns = [
    path('', views.resources_list_view, name='resources'),
]
