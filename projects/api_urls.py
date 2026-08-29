from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Project
from .serializers import ProjectSerializer

class ProjectsAPIView(APIView):
    def get(self, request):
        difficulty = request.GET.get('difficulty')
        qs = Project.objects.prefetch_related('skills').all()
        if difficulty:
            qs = qs.filter(difficulty=difficulty)
        return Response(ProjectSerializer(qs, many=True).data)

urlpatterns = [
    path('', ProjectsAPIView.as_view(), name='api_projects'),
]
