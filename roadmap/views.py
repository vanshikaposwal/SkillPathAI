from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Roadmap, Milestone, RoadmapItem, Progress
from recommendations.recommendation_engine import generate_recommendations_for_user

@login_required
def roadmap_view(request):
    roadmap = Roadmap.objects.filter(user=request.user).order_by('-created_at').first()
    if not roadmap:
        roadmap = generate_recommendations_for_user(request.user)
    
    milestones = roadmap.milestones.prefetch_related('items', 'items__skill', 'items__resource', 'items__project').all()
    
    return render(request, 'roadmap/roadmap.html', {
        'roadmap': roadmap,
        'milestones': milestones,
    })

@login_required
def roadmap_detail_view(request, pk):
    roadmap = get_object_or_404(Roadmap, pk=pk, user=request.user)
    milestones = roadmap.milestones.prefetch_related('items', 'items__skill', 'items__resource').all()
    return render(request, 'roadmap/roadmap_detail.html', {
        'roadmap': roadmap,
        'milestones': milestones,
    })
