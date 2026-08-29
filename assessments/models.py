from django.db import models
from django.contrib.auth.models import User
from careers.models import Skill
from roadmap.models import Milestone

class Assessment(models.Model):
    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, null=True, blank=True, related_name='assessments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='assessments')
    passing_score = models.IntegerField(default=70)

    def __str__(self):
        return self.title

    @property
    def questions_count(self):
        return self.questions.count()

class Question(models.Model):
    CORRECT_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=CORRECT_CHOICES)
    explanation = models.TextField(help_text='Detailed concept explanation shown upon completion.')

    def __str__(self):
        return f'{self.assessment.title}: {self.question[:60]}...'

class AssessmentAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assessment_attempts')
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='attempts')
    score = models.FloatField(default=0.0)
    passed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f'{self.user.username} scored {self.score}% on {self.assessment.title}'
