from rest_framework import serializers
from .models import LearningResource
from careers.serializers import SkillSerializer

class LearningResourceSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_name = serializers.ReadOnlyField(source='skill.name')

    class Meta:
        model = LearningResource
        fields = [
            'id', 'title', 'description', 'resource_type', 'platform',
            'url', 'skill', 'skill_name', 'difficulty', 'estimated_hours',
            'free_or_paid', 'rating'
        ]
