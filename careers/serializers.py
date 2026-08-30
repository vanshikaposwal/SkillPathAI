from rest_framework import serializers
from .models import Skill, Career, CareerSkill

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'name', 'description', 'category']

class CareerSkillSerializer(serializers.ModelSerializer):
    skill = SkillSerializer(read_only=True)
    skill_id = serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all(), source='skill', write_only=True)

    class Meta:
        model = CareerSkill
        fields = ['id', 'career', 'skill', 'skill_id', 'required_level', 'importance', 'prerequisite_order']

class CareerSerializer(serializers.ModelSerializer):
    career_skills = CareerSkillSerializer(many=True, read_only=True)

    class Meta:
        model = Career
        fields = ['id', 'name', 'description', 'category', 'icon', 'average_salary', 'market_demand', 'career_skills']
