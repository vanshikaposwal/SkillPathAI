from django.db import models
from careers.models import Skill

class Project(models.Model):
    DIFFICULTY_CHOICES = [
        ('Beginner', 'Beginner (Foundational)'),
        ('Intermediate', 'Intermediate (Practical Architecture)'),
        ('Advanced', 'Advanced (Production Scalability)'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='Intermediate')
    estimated_hours = models.IntegerField(default=12)
    skills = models.ManyToManyField(Skill, related_name='projects')
    prerequisites = models.TextField(blank=True, help_text="e.g. Basic Java, SQL, REST knowledge")
    starter_guide = models.TextField(blank=True, help_text="Step-by-step implementation milestones")
    github_template_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['difficulty', 'title']

    def __str__(self):
        return f"{self.title} ({self.difficulty})"
