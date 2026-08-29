from rest_framework import serializers
from .models import Roadmap, Milestone, RoadmapItem, Progress, Feedback
from careers.serializers import CareerSerializer, SkillSerializer
from resources.serializers import LearningResourceSerializer
from projects.serializers import ProjectSerializer

class RoadmapItemSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    resource = LearningResourceSerializer(read_only=True)
    project = ProjectSerializer(read_only=True)

    class Meta:
        model = RoadmapItem
        fields = [
            'id', 'milestone', 'title', 'item_type', 'description',
            'skill', 'resource', 'project', 'estimated_hours',
            'order', 'status', 'why_recommended'
        ]

class MilestoneSerializer(serializers.ModelSerializer):
    items = RoadmapItemSerializer(many=True, read_only=True)

    class Meta:
        model = Milestone
        fields = [
            'id', 'roadmap', 'title', 'description', 'order',
            'estimated_hours', 'progress_percentage', 'items_count',
            'completed_count', 'is_completed', 'items'
        ]

class RoadmapSerializer(serializers.ModelSerializer):
    career = CareerSerializer(read_only=True)
    milestones = MilestoneSerializer(many=True, read_only=True)

    class Meta:
        model = Roadmap
        fields = [
            'id', 'user', 'career', 'title', 'description',
            'total_estimated_hours', 'total_items_count',
            'completed_items_count', 'progress_percentage',
            'milestones', 'created_at', 'updated_at'
        ]

class ProgressSerializer(serializers.ModelSerializer):
    item_title = serializers.ReadOnlyField(source='roadmap_item.title')

    class Meta:
        model = Progress
        fields = ['id', 'user', 'roadmap_item', 'item_title', 'completed_at', 'learning_minutes']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'roadmap_item', 'feedback_type', 'user_note', 'created_at']
        read_only_fields = ['user']
