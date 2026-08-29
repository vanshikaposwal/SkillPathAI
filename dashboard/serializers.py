from rest_framework import serializers

class DashboardAnalyticsSerializer(serializers.Serializer):
    overall_progress = serializers.IntegerField()
    skills_acquired = serializers.IntegerField()
    total_skills = serializers.IntegerField()
    current_milestone_number = serializers.IntegerField()
    total_milestones = serializers.IntegerField()
    current_milestone_title = serializers.CharField()
    weekly_hours_logged = serializers.FloatField()
    weekly_hours_target = serializers.FloatField()
    streak_days = serializers.IntegerField()
    next_best_action = serializers.DictField()
    radar_chart_data = serializers.DictField()
    milestones_progress_data = serializers.DictField()
