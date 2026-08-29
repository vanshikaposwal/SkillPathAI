from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from learners.models import LearnerProfile, UserSkill
from roadmap.models import Roadmap, Milestone, RoadmapItem, Progress
from careers.models import Career, Skill, CareerSkill
from recommendations.recommendation_engine import generate_recommendations_for_user, calculate_skill_gaps, match_target_career

def compute_dashboard_data(user):
    profile, _ = LearnerProfile.objects.get_or_create(user=user)
    career_name = match_target_career(profile.career_goal)
    career, _ = Career.objects.get_or_create(name=career_name)
    
    roadmap = Roadmap.objects.filter(user=user).order_by('-created_at').first()
    if not roadmap or not roadmap.milestones.exists():
        roadmap = generate_recommendations_for_user(user)

    total_items = roadmap.total_items_count
    completed_items = roadmap.completed_items_count
    overall_progress = roadmap.progress_percentage

    milestones = roadmap.milestones.prefetch_related('items').all()
    total_milestones = milestones.count()
    active_m = milestones.filter(items__status__in=['Not Started', 'In Progress']).first() or milestones.last()
    current_milestone_number = active_m.order if active_m else 1
    current_milestone_title = active_m.title if active_m else "Milestone 1"

    next_item = None
    if active_m:
        next_item = active_m.items.filter(status__in=['Not Started', 'In Progress']).first()
    if not next_item:
        next_item = RoadmapItem.objects.filter(milestone__roadmap=roadmap, status__in=['Not Started', 'In Progress']).first()

    career_skills = CareerSkill.objects.filter(career=career).select_related('skill')
    total_career_skills = career_skills.count() or 12
    user_skills = {us.skill_id: us.proficiency for us in UserSkill.objects.filter(user=user)}
    acquired_count = sum(1 for cs in career_skills if cs.skill_id in user_skills and user_skills[cs.skill_id] in ['Intermediate', 'Advanced'])

    weekly_target = 10.0
    if profile.weekly_hours == '1-5': weekly_target = 5.0
    elif profile.weekly_hours == '5-10': weekly_target = 10.0
    elif profile.weekly_hours == '10-15': weekly_target = 15.0
    elif profile.weekly_hours == '15-20': weekly_target = 20.0
    elif profile.weekly_hours == '20+': weekly_target = 25.0
    weekly_logged = 6.5

    radar_labels = []
    radar_user_scores = []
    radar_target_scores = []
    prof_map = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}

    sample_cs = career_skills[:7]
    for cs in sample_cs:
        radar_labels.append(cs.skill.name)
        radar_target_scores.append(prof_map.get(cs.required_level, 3))
        user_prof = user_skills.get(cs.skill_id, 'None')
        radar_user_scores.append(prof_map.get(user_prof, 0))

    if not radar_labels:
        radar_labels = ['Java/Python', 'SQL & DB', 'REST APIs', 'Spring/Django', 'Docker', 'Testing']
        radar_user_scores = [3, 2, 2, 1, 1, 1]
        radar_target_scores = [3, 3, 3, 3, 2, 2]

    milestone_labels = [f"M{m.order}" for m in milestones]
    milestone_pcts = [m.progress_percentage for m in milestones]

    return {
        'profile': profile,
        'career': career,
        'roadmap': roadmap,
        'overall_progress': overall_progress,
        'completed_items': completed_items,
        'total_items': total_items,
        'skills_acquired': acquired_count,
        'total_skills': total_career_skills,
        'current_milestone_number': current_milestone_number,
        'total_milestones': total_milestones,
        'current_milestone_title': current_milestone_title,
        'weekly_hours_logged': weekly_logged,
        'weekly_hours_target': weekly_target,
        'streak_days': profile.streak_days,
        'next_best_action': next_item,
        'milestones': milestones,
        'radar_labels': radar_labels,
        'radar_user_scores': radar_user_scores,
        'radar_target_scores': radar_target_scores,
        'milestone_labels': milestone_labels,
        'milestone_pcts': milestone_pcts,
    }

@login_required
def dashboard_view(request):
    data = compute_dashboard_data(request.user)
    return render(request, 'dashboard/dashboard.html', data)
