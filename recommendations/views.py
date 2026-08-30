from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import get_user_skill_gaps_data

@login_required
def skill_gaps_view(request):
    data = get_user_skill_gaps_data(request.user)
    return render(request, 'recommendations/skill_gaps.html', data)
