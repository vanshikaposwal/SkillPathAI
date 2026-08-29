from django import forms
from .models import LearnerProfile, UserSkill

class LearnerProfileForm(forms.ModelForm):
    class Meta:
        model = LearnerProfile
        fields = ['career_goal', 'experience_level', 'weekly_hours', 'target_timeline', 'learning_style', 'interests', 'learning_history']
        widgets = {
            'career_goal': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'e.g. Java Backend Developer, AI Engineer, Full Stack...'}),
            'experience_level': forms.Select(attrs={'class': 'form-select'}),
            'weekly_hours': forms.Select(attrs={'class': 'form-select'}),
            'target_timeline': forms.Select(attrs={'class': 'form-select'}),
            'learning_style': forms.Select(attrs={'class': 'form-select'}),
            'interests': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. Microservices, Cloud Architecture, Open Source...'}),
            'learning_history': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'e.g. Completed CS50, built CRUD blog in Django...'}),
        }

class UserSkillForm(forms.ModelForm):
    class Meta:
        model = UserSkill
        fields = ['skill', 'proficiency', 'experience_months']
        widgets = {
            'skill': forms.Select(attrs={'class': 'form-select'}),
            'proficiency': forms.Select(attrs={'class': 'form-select'}),
            'experience_months': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
