from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import LearningResource
from .serializers import LearningResourceSerializer

class LearningResourcesAPIView(APIView):
    def get(self, request):
        skill_id = request.GET.get('skill_id')
        res_type = request.GET.get('type')
        qs = LearningResource.objects.select_related('skill').all()
        if skill_id:
            qs = qs.filter(skill_id=skill_id)
        if res_type:
            qs = qs.filter(resource_type=res_type)
        return Response(LearningResourceSerializer(qs, many=True).data)

urlpatterns = [
    path('', LearningResourcesAPIView.as_view(), name='api_resources'),
]
