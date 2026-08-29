from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Roadmap, Milestone, RoadmapItem, Progress, Feedback
from .serializers import RoadmapSerializer, RoadmapItemSerializer, ProgressSerializer, FeedbackSerializer
from .services import handle_adaptive_feedback
from recommendations.recommendation_engine import generate_recommendations_for_user

class RoadmapListAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        roadmaps = Roadmap.objects.filter(user=request.user)
        return Response(RoadmapSerializer(roadmaps, many=True).data)

class RoadmapGenerateAPIView(APIView):
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        roadmap = generate_recommendations_for_user(request.user, force_regenerate=True)
        return Response(RoadmapSerializer(roadmap).data, status=status.HTTP_201_CREATED)

class RoadmapDetailAPIView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            roadmap = Roadmap.objects.get(pk=pk, user=request.user)
            return Response(RoadmapSerializer(roadmap).data)
        except Roadmap.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

class RoadmapItemCompleteAPIView(APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            item = RoadmapItem.objects.get(pk=pk, milestone__roadmap__user=request.user)
            item.status = 'Completed'
            item.save()
            progress, _ = Progress.objects.get_or_create(
                user=request.user,
                roadmap_item=item,
                defaults={'learning_minutes': int(item.estimated_hours * 60)}
            )
            roadmap = item.milestone.roadmap
            return Response({
                'success': True,
                'status': item.status,
                'progress_percentage': roadmap.progress_percentage,
                'completed_items': roadmap.completed_items_count,
                'total_items': roadmap.total_items_count
            })
        except RoadmapItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

class RoadmapItemFeedbackAPIView(APIView):
    def post(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        feedback_type = request.data.get('feedback_type')
        user_note = request.data.get('user_note', '')
        if not feedback_type:
            return Response({'error': 'feedback_type is required'}, status=status.HTTP_400_BAD_REQUEST)
        result = handle_adaptive_feedback(request.user, pk, feedback_type, user_note)
        return Response(result, status=status.HTTP_200_OK if result['success'] else status.HTTP_400_BAD_REQUEST)

class RoadmapItemWhyAPIView(APIView):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            item = RoadmapItem.objects.get(pk=pk, milestone__roadmap__user=request.user)
            return Response({
                'id': item.id,
                'title': item.title,
                'why_recommended': item.why_recommended or "Recommended based on your target career skill graph and current proficiency gaps."
            })
        except RoadmapItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)

urlpatterns = [
    path('', RoadmapListAPIView.as_view(), name='api_roadmap_list'),
    path('generate/', RoadmapGenerateAPIView.as_view(), name='api_roadmap_generate'),
    path('<int:pk>/', RoadmapDetailAPIView.as_view(), name='api_roadmap_detail'),
    path('item/<int:pk>/complete/', RoadmapItemCompleteAPIView.as_view(), name='api_item_complete'),
    path('item/<int:pk>/feedback/', RoadmapItemFeedbackAPIView.as_view(), name='api_item_feedback'),
    path('item/<int:pk>/why/', RoadmapItemWhyAPIView.as_view(), name='api_item_why'),
]
