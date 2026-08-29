from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LearnerProfile, UserSkill
from .serializers import LearnerProfileSerializer, UserSkillSerializer, ProfileAnalysisRequestSerializer
from ai_assistant.services import analyze_career_goal_with_ai

class ProfileAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        profile, _ = LearnerProfile.objects.get_or_create(user=request.user)
        return Response(LearnerProfileSerializer(profile).data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        profile, _ = LearnerProfile.objects.get_or_create(user=request.user)
        serializer = LearnerProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProfileAnalyzeAPIView(APIView):
    def post(self, request):
        serializer = ProfileAnalysisRequestSerializer(data=request.data)
        if serializer.is_valid():
            goal = serializer.validated_data['career_goal']
            exp = serializer.validated_data.get('experience_level', 'Intermediate')
            result = analyze_career_goal_with_ai(goal, exp)
            return Response(result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserSkillsAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response([])
        skills = UserSkill.objects.filter(user=request.user)
        return Response(UserSkillSerializer(skills, many=True).data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSkillSerializer(data=request.data)
        if serializer.is_valid():
            skill_inst = serializer.validated_data['skill']
            user_skill, created = UserSkill.objects.update_or_create(
                user=request.user,
                skill=skill_inst,
                defaults={
                    'proficiency': serializer.validated_data.get('proficiency', 'Intermediate'),
                    'experience_months': serializer.validated_data.get('experience_months', 6)
                }
            )
            return Response(UserSkillSerializer(user_skill).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

urlpatterns = [
    path('', ProfileAPIView.as_view(), name='api_profile'),
    path('analyze/', ProfileAnalyzeAPIView.as_view(), name='api_profile_analyze'),
    path('skills/', UserSkillsAPIView.as_view(), name='api_user_skills'),
]
