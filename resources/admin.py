from django.contrib import admin
from .models import LearningResource

@admin.register(LearningResource)
class LearningResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'platform', 'skill', 'resource_type', 'difficulty', 'estimated_hours', 'free_or_paid', 'rating']
    list_filter = ['resource_type', 'platform', 'difficulty', 'free_or_paid', 'skill']
    search_fields = ['title', 'description', 'platform']
