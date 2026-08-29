from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Assessment, Question, AssessmentAttempt
from .serializers import AssessmentSerializer, QuestionSerializer
from roadmap.models import RoadmapItem, Progress

class AssessmentDetailAPIView(APIView):
    def get(self, request, pk):
        try:
            assessment = Assessment.objects.get(pk=pk)
            return Response(AssessmentSerializer(assessment).data)
        except Assessment.DoesNotExist:
            return Response({'error': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)

class AssessmentSubmitAPIView(APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            assessment = Assessment.objects.get(pk=pk)
            answers = request.data.get('answers', {})
            questions = assessment.questions.all()
            total = questions.count()
            correct = 0
            feedback = []
            
            for q in questions:
                user_ans = answers.get(str(q.id))
                is_correct = (user_ans == q.correct_answer)
                if is_correct:
                    correct += 1
                feedback.append({
                    'question_id': q.id,
                    'user_answer': user_ans,
                    'correct_answer': q.correct_answer,
                    'is_correct': is_correct,
                    'explanation': q.explanation
                })
                
            score = int((correct / total * 100)) if total > 0 else 100
            passed = score >= assessment.passing_score
            
            attempt = AssessmentAttempt.objects.create(
                user=request.user,
                assessment=assessment,
                score=score,
                passed=passed
            )
            
            if assessment.milestone:
                item = RoadmapItem.objects.filter(milestone=assessment.milestone, item_type='Assessment').first()
                if item:
                    item.status = 'Completed'
                    item.save()
                    Progress.objects.get_or_create(user=request.user, roadmap_item=item)

            return Response({
                'score': score,
                'passed': passed,
                'correct_count': correct,
                'total_questions': total,
                'feedback': feedback
            })
        except Assessment.DoesNotExist:
            return Response({'error': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)

urlpatterns = [
    path('<int:pk>/', AssessmentDetailAPIView.as_view(), name='api_assessment_detail'),
    path('<int:pk>/submit/', AssessmentSubmitAPIView.as_view(), name='api_assessment_submit'),
]
