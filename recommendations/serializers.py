from rest_framework import serializers

class SkillGapItemSerializer(serializers.Serializer):
    skill_id = serializers.IntegerField()
    skill_name = serializers.CharField()
    category = serializers.CharField()
    current_level = serializers.CharField()
    current_percent = serializers.IntegerField()
    required_level = serializers.CharField()
    importance = serializers.CharField()
    gap_score = serializers.IntegerField()
    priority = serializers.CharField()
    prerequisite_order = serializers.IntegerField()
    why_it_matters = serializers.CharField()

class SkillGapsResponseSerializer(serializers.Serializer):
    target_career = serializers.CharField()
    gaps = SkillGapItemSerializer(many=True)
    high_priority_count = serializers.IntegerField()
    medium_priority_count = serializers.IntegerField()
    acquired_count = serializers.IntegerField()
