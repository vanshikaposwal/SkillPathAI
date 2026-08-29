from rest_framework import serializers
from .models import Project
from careers.serializers import SkillSerializer

class ProjectSerializer(serializers.ModelSerializer):
    skills = SkillSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'difficulty', 'estimated_hours', 'skills', 'prerequisites', 'starter_guide', 'github_template_url']
