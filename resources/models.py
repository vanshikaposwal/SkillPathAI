from django.db import models
from careers.models import Skill

class LearningResource(models.Model):
    TYPE_CHOICES = [
        ('Video', 'Video'),
        ('Course', 'Course'),
        ('Documentation', 'Official Documentation'),
        ('Article', 'Article / Guide'),
        ('Practice', 'Practice / Exercises'),
        ('Project', 'Guided Project'),
    ]
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    FREE_PAID_CHOICES = [
        ('Free', 'Free'),
        ('Paid', 'Paid'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    resource_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='Documentation')
    platform = models.CharField(max_length=100, default='Official Docs', help_text="e.g. MDN, freeCodeCamp, Kaggle, LeetCode")
    url = models.URLField(max_length=500)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='resources')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Intermediate')
    estimated_hours = models.FloatField(default=2.0)
    free_or_paid = models.CharField(max_length=10, choices=FREE_PAID_CHOICES, default='Free')
    rating = models.FloatField(default=4.8)

    class Meta:
        ordering = ['skill', 'difficulty', 'title']

    def __str__(self):
        return f"[{self.platform}] {self.title} ({self.skill.name})"
