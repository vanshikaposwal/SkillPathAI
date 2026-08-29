from rest_framework import serializers
from .models import LearnerProfile, UserSkill
from careers.serializers import SkillSerializer
from careers.models import Skill

class UserSkillSerializer(serializers.ModelSerializer):
    skill_name = serializers.ReadOnlyField(source='skill.name')
    skill_category = serializers.ReadOnlyField(source='skill.category')
    skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), source='skill', write_only=True)

    class Meta:
        model = UserSkill
        fields = ['id', 'skill', 'skill_id', 'skill_name', 'skill_category', 'proficiency', 'experience_months', 'proficiency_percent']
        read_only_fields = ['skill']

class LearnerProfileSerializer(serializers.ModelSerializer):
    user_skills = serializers.SerializerMethodField()

    class Meta:
        model = LearnerProfile
        fields = [
            'id', 'career_goal', 'experience_level', 'weekly_hours',
            'target_timeline', 'learning_style', 'interests',
            'learning_history', 'streak_days', 'user_skills', 'created_at', 'updated_at'
        ]

    def get_user_skills(self, obj):
        skills = UserSkill.objects.filter(user=obj.user)
        return UserSkillSerializer(skills, many=True).data

class ProfileAnalysisRequestSerializer(serializers.Serializer):
    career_goal = serializers.CharField(required=True)
    experience_level = serializers.CharField(required=False, default='Intermediate')
    skills = serializers.ListField(child=serializers.CharField(), required=False, default=list)
    interests = serializers.CharField(required=False, allow_blank=True)
    weekly_hours = serializers.CharField(required=False, default='5-10')
    target_timeline = serializers.CharField(required=False, default='3 months')
