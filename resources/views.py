from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import LearningResource
from careers.models import Skill
from learners.models import UserSkill

@login_required
def resources_list_view(request):
    query = request.GET.get('q', '')
    res_type = request.GET.get('type', '')
    skill_id = request.GET.get('skill', '')
    free_paid = request.GET.get('cost', '')
    
    resources = LearningResource.objects.select_related('skill').all()
    if query:
        resources = resources.filter(title__icontains=query) | resources.filter(description__icontains=query)
    if res_type:
        resources = resources.filter(resource_type=res_type)
    if skill_id:
        resources = resources.filter(skill_id=skill_id)
    if free_paid:
        resources = resources.filter(free_or_paid=free_paid)
        
    skills = Skill.objects.all().order_by('name')
    
    return render(request, 'recommendations/resources.html', {
        'resources': resources,
        'skills': skills,
        'selected_type': res_type,
        'selected_skill': int(skill_id) if skill_id.isdigit() else '',
        'selected_cost': free_paid,
        'query': query,
    })
