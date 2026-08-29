from django.contrib import admin
from .models import LearnerProfile, UserSkill

@admin.register(LearnerProfile)
class LearnerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'career_goal', 'experience_level', 'weekly_hours', 'target_timeline', 'learning_style']
    search_fields = ['user__username', 'career_goal', 'interests']
    list_filter = ['experience_level', 'weekly_hours', 'learning_style']

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'proficiency', 'experience_months']
    list_filter = ['proficiency', 'skill']
    search_fields = ['user__username', 'skill__name']
