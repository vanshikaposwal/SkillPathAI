from django.contrib import admin
from .models import Roadmap, Milestone, RoadmapItem, Progress, Feedback

class RoadmapItemInline(admin.TabularInline):
    model = RoadmapItem
    extra = 1

@admin.register(Milestone)
class MilestoneAdmin(admin.ModelAdmin):
    list_display = ['title', 'roadmap', 'order', 'estimated_hours', 'progress_percentage']
    list_filter = ['roadmap__career']
    inlines = [RoadmapItemInline]

class MilestoneInline(admin.TabularInline):
    model = Milestone
    extra = 1

@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'career', 'progress_percentage', 'created_at']
    list_filter = ['career']
    search_fields = ['title', 'user__username']
    inlines = [MilestoneInline]

@admin.register(RoadmapItem)
class RoadmapItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'milestone', 'item_type', 'status', 'order']
    list_filter = ['item_type', 'status']
    search_fields = ['title', 'description']

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'roadmap_item', 'completed_at', 'learning_minutes']
    list_filter = ['completed_at']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['user', 'roadmap_item', 'feedback_type', 'created_at']
    list_filter = ['feedback_type', 'created_at']
