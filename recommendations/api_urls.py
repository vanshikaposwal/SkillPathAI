from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_user_skill_gaps_data
from .serializers import SkillGapsResponseSerializer

class SkillGapsAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        data = get_user_skill_gaps_data(request.user)
        res = {
            'target_career': data['target_career'],
            'gaps': data['gaps'],
            'high_priority_count': data['high_priority_count'],
            'medium_priority_count': data['medium_priority_count'],
            'acquired_count': data['acquired_count']
        }
        return Response(res)

urlpatterns = [
    path('', SkillGapsAPIView.as_view(), name='api_skill_gaps'),
]
