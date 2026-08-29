from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import LearnerProfile, UserSkill
from .forms import LearnerProfileForm
from careers.models import Skill, Career
from recommendations.recommendation_engine import generate_recommendations_for_user

@login_required
def onboarding_start(request):
    return redirect('onboarding_step', step=1)

@login_required
def onboarding_step_view(request, step):
    profile, _ = LearnerProfile.objects.get_or_create(user=request.user)
    skills = Skill.objects.all().order_by('category', 'name')
    user_skills = UserSkill.objects.filter(user=request.user)
    
    if request.method == 'POST':
        if step == 1:
            goal = request.POST.get('career_goal', '').strip()
            if goal:
                profile.career_goal = goal
                profile.save()
            return redirect('onboarding_step', step=2)
        elif step == 2:
            exp = request.POST.get('experience_level', 'Intermediate')
            profile.experience_level = exp
            profile.save()
            return redirect('onboarding_step', step=3)
        elif step == 3:
            # Save selected skills
            skill_ids = request.POST.getlist('skills[]')
            # Clear old and add new
            UserSkill.objects.filter(user=request.user).delete()
            for sid in skill_ids:
                try:
                    s_obj = Skill.objects.get(id=sid)
                    prof = request.POST.get(f'prof_{sid}', 'Intermediate')
                    UserSkill.objects.create(user=request.user, skill=s_obj, proficiency=prof)
                except Skill.DoesNotExist:
                    pass
            return redirect('onboarding_step', step=4)
        elif step == 4:
            history = request.POST.get('learning_history', '')
            interests = request.POST.get('interests', '')
            profile.learning_history = history
            profile.interests = interests
            profile.save()
            return redirect('onboarding_step', step=5)
        elif step == 5:
            profile.weekly_hours = request.POST.get('weekly_hours', '5-10')
            profile.learning_style = request.POST.get('learning_style', 'Mixed')
            profile.target_timeline = request.POST.get('target_timeline', '3 months')
            profile.save()
            
            # Trigger recommendation engine!
            generate_recommendations_for_user(request.user)
            messages.success(request, "Your AI-powered personalized learning roadmap has been generated!")
            return redirect('dashboard')

    step_templates = {
        1: 'onboarding/career_goal.html',
        2: 'onboarding/profile.html',
        3: 'onboarding/skills.html',
        4: 'onboarding/profile.html',
        5: 'onboarding/preferences.html',
    }
    
    context = {
        'step': step,
        'profile': profile,
        'skills': skills,
        'user_skills': user_skills,
        'careers': Career.objects.all(),
    }
    return render(request, step_templates.get(step, 'onboarding/career_goal.html'), context)

@login_required
def profile_view(request):
    profile, _ = LearnerProfile.objects.get_or_create(user=request.user)
    user_skills = UserSkill.objects.filter(user=request.user).select_related('skill')
    all_skills = Skill.objects.all().order_by('category', 'name')
    
    return render(request, 'profile/profile.html', {
        'profile': profile,
        'user_skills': user_skills,
        'all_skills': all_skills,
    })

@login_required
def edit_profile_view(request):
    profile, _ = LearnerProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = LearnerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = LearnerProfileForm(instance=profile)
    return render(request, 'profile/profile.html', {'profile': profile, 'form': form, 'edit_mode': True})

@login_required
def regenerate_path_view(request):
    if request.method == 'POST':
        generate_recommendations_for_user(request.user, force_regenerate=True)
        messages.success(request, "Your learning roadmap has been regenerated with updated profile data!")
    return redirect('dashboard')
