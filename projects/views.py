from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Project
from careers.models import Skill

@login_required
def projects_list_view(request):
    difficulty = request.GET.get('diff', '')
    skill_id = request.GET.get('skill', '')
    
    projects = Project.objects.prefetch_related('skills').all()
    if difficulty:
        projects = projects.filter(difficulty=difficulty)
    if skill_id:
        projects = projects.filter(skills__id=skill_id)
        
    skills = Skill.objects.all().order_by('name')
    return render(request, 'recommendations/projects.html', {
        'projects': projects,
        'skills': skills,
        'selected_diff': difficulty,
        'selected_skill': int(skill_id) if skill_id.isdigit() else '',
    })
