from rest_framework import serializers
from .models import Assessment, Question, AssessmentAttempt

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'explanation']

class QuestionPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'question', 'option_a', 'option_b', 'option_c', 'option_d']

class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionPublicSerializer(many=True, read_only=True)
    questions_count = serializers.ReadOnlyField()

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'passing_score', 'questions_count', 'questions']

class AssessmentAttemptSerializer(serializers.ModelSerializer):
    assessment_title = serializers.ReadOnlyField(source='assessment.title')

    class Meta:
        model = AssessmentAttempt
        fields = ['id', 'assessment', 'assessment_title', 'score', 'passed', 'completed_at']
