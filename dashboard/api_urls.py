from django.urls import path
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .views import compute_dashboard_data

class DashboardStatsAPIView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        data = compute_dashboard_data(request.user)
        nba = data['next_best_action']
        return Response({
            'overall_progress': data['overall_progress'],
            'completed_items': data['completed_items'],
            'total_items': data['total_items'],
            'skills_acquired': data['skills_acquired'],
            'total_skills': data['total_skills'],
            'current_milestone_number': data['current_milestone_number'],
            'total_milestones': data['total_milestones'],
            'weekly_hours_logged': data['weekly_hours_logged'],
            'weekly_hours_target': data['weekly_hours_target'],
            'streak_days': data['streak_days'],
            'next_best_action': {
                'id': nba.id if nba else None,
                'title': nba.title if nba else 'Review Roadmap',
                'estimated_hours': nba.estimated_hours if nba else 1.0,
                'why_recommended': nba.why_recommended if nba else '',
            } if nba else None,
            'radar_chart': {
                'labels': data['radar_labels'],
                'user_scores': data['radar_user_scores'],
                'target_scores': data['radar_target_scores'],
            },
            'milestones_chart': {
                'labels': data['milestone_labels'],
                'progress_pcts': data['milestone_pcts'],
            }
        })

urlpatterns = [
    path('', DashboardStatsAPIView.as_view(), name='api_dashboard_stats'),
]
