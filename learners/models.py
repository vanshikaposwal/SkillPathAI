from django.db import models
from django.contrib.auth.models import User
from careers.models import Skill

class LearnerProfile(models.Model):
    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner (No prior tech experience)'),
        ('Intermediate', 'Intermediate (Some coding / related degree)'),
        ('Advanced', 'Advanced (Industry experience / solid foundation)'),
        ('Professional', 'Professional (Looking to switch or level up)'),
    ]
    WEEKLY_HOURS_CHOICES = [
        ('1-5', '1–5 hours (Casual pace)'),
        ('5-10', '5–10 hours (Standard pace)'),
        ('10-15', '10–15 hours (Accelerated pace)'),
        ('15-20', '15–20 hours (Intensive pace)'),
        ('20+', '20+ hours (Full-time bootcamp pace)'),
    ]
    TIMELINE_CHOICES = [
        ('1 month', '1 Month (Rapid / Sprint)'),
        ('3 months', '3 Months (Recommended standard)'),
        ('6 months', '6 Months (Comprehensive mastery)'),
        ('1 year', '1 Year (Deep long-term track)'),
    ]
    STYLE_CHOICES = [
        ('Videos', 'Video Tutorials & Walkthroughs'),
        ('Reading', 'Documentation & In-depth Articles'),
        ('Practice', 'Hands-on Coding Challenges & Katas'),
        ('Projects', 'Project-based Building'),
        ('Mixed', 'Balanced Mix of All Methods'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='learner_profile')
    career_goal = models.CharField(max_length=255, default='Backend Developer')
    experience_level = models.CharField(max_length=30, choices=EXPERIENCE_CHOICES, default='Intermediate')
    weekly_hours = models.CharField(max_length=20, choices=WEEKLY_HOURS_CHOICES, default='5-10')
    target_timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES, default='3 months')
    learning_style = models.CharField(max_length=20, choices=STYLE_CHOICES, default='Mixed')
    interests = models.TextField(blank=True, help_text="e.g. Distributed Systems, AI Apps, Web Dev")
    learning_history = models.TextField(blank=True, help_text="e.g. Completed Python 101, built portfolio website")
    streak_days = models.IntegerField(default=7)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile -> {self.career_goal}"

class UserSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner (Familiar with basics)'),
        ('Intermediate', 'Intermediate (Can build apps/features)'),
        ('Advanced', 'Advanced (Production mastery)'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='learner_skills')
    proficiency = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='Intermediate')
    experience_months = models.IntegerField(default=6)

    class Meta:
        unique_together = ('user', 'skill')
        ordering = ['skill__name']

    def __str__(self):
        return f"{self.user.username} - {self.skill.name}: {self.proficiency}"

    @property
    def proficiency_score(self):
        scores = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
        return scores.get(self.proficiency, 1)

    @property
    def proficiency_percent(self):
        pcts = {'Beginner': 40, 'Intermediate': 70, 'Advanced': 95}
        return pcts.get(self.proficiency, 40)
