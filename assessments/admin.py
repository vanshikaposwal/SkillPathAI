from django.contrib import admin
from .models import Assessment, Question, AssessmentAttempt

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'milestone', 'passing_score', 'questions_count']
    inlines = [QuestionInline]

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['assessment', 'question', 'correct_answer']
    search_fields = ['question', 'explanation']

@admin.register(AssessmentAttempt)
class AssessmentAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'assessment', 'score', 'passed', 'completed_at']
    list_filter = ['passed', 'completed_at']
