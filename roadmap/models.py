from django.db import models
from django.contrib.auth.models import User
from careers.models import Career, Skill
from resources.models import LearningResource
from projects.models import Project

class Roadmap(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='roadmaps')
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='roadmaps')
    title = models.CharField(max_length=255)
    description = models.TextField()
    total_estimated_hours = models.IntegerField(default=120)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.title}"

    @property
    def total_items_count(self):
        return sum(m.items.count() for m in self.milestones.all())

    @property
    def completed_items_count(self):
        return sum(m.items.filter(status='Completed').count() for m in self.milestones.all())

    @property
    def progress_percentage(self):
        total = self.total_items_count
        if total == 0:
            return 0
        return int((self.completed_items_count / total) * 100)

class Milestone(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=255)
    description = models.TextField()
    order = models.IntegerField(default=1)
    estimated_hours = models.IntegerField(default=30)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Milestone {self.order}: {self.title} ({self.roadmap.user.username})"

    @property
    def items_count(self):
        return self.items.count()

    @property
    def completed_count(self):
        return self.items.filter(status='Completed').count()

    @property
    def progress_percentage(self):
        total = self.items_count
        if total == 0:
            return 0
        return int((self.completed_count / total) * 100)

    @property
    def is_completed(self):
        total = self.items_count
        return total > 0 and self.completed_count == total

class RoadmapItem(models.Model):
    ITEM_TYPE_CHOICES = [
        ('Topic', 'Core Topic / Concept'),
        ('Resource', 'Curated Learning Resource'),
        ('Project', 'Hands-on Project'),
        ('Assessment', 'Milestone Assessment'),
    ]
    STATUS_CHOICES = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Skipped', 'Skipped'),
    ]

    milestone = models.ForeignKey(Milestone, on_delete=models.CASCADE, related_name='items')
    title = models.CharField(max_length=255)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='Topic')
    description = models.TextField()
    skill = models.ForeignKey(Skill, on_delete=models.SET_NULL, null=True, blank=True, related_name='roadmap_items')
    resource = models.ForeignKey(LearningResource, on_delete=models.SET_NULL, null=True, blank=True, related_name='roadmap_items')
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='roadmap_items')
    estimated_hours = models.FloatField(default=2.0)
    order = models.IntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Not Started')
    why_recommended = models.TextField(blank=True, help_text="AI-generated personalized rationale")

    class Meta:
        ordering = ['milestone__order', 'order']

    def __str__(self):
        return f"{self.title} [{self.status}] (M{self.milestone.order})"

class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress_records')
    roadmap_item = models.ForeignKey(RoadmapItem, on_delete=models.CASCADE, related_name='progress_records')
    completed_at = models.DateTimeField(auto_now_add=True)
    learning_minutes = models.IntegerField(default=45)

    class Meta:
        ordering = ['-completed_at']

    def __str__(self):
        return f"{self.user.username} completed {self.roadmap_item.title}"

class Feedback(models.Model):
    FEEDBACK_TYPES = [
        ('TOO_EASY', 'Too Easy — Fast track / Skip introductory material'),
        ('TOO_DIFFICULT', 'Too Difficult — Need prerequisite resources'),
        ('ALREADY_KNOW', 'Already Know — Mark completed/skip'),
        ('NOT_INTERESTED', 'Not Interested — Deprioritize / Suggest alternatives'),
        ('MORE_PRACTICE', 'More Practice — Add coding exercises'),
        ('NEED_EXPLANATION', 'Need Explanation — Clarify concept in depth'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='feedbacks')
    roadmap_item = models.ForeignKey(RoadmapItem, on_delete=models.CASCADE, related_name='feedbacks')
    feedback_type = models.CharField(max_length=30, choices=FEEDBACK_TYPES)
    user_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} on {self.roadmap_item.title}: {self.feedback_type}"
