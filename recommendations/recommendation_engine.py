import re
from django.contrib.auth.models import User
from careers.models import Career, Skill, CareerSkill
from learners.models import LearnerProfile, UserSkill
from roadmap.models import Roadmap, Milestone, RoadmapItem, Progress
from resources.models import LearningResource
from projects.models import Project
from assessments.models import Assessment
from .skill_graph import CAREER_SKILL_GRAPHS
from ai_assistant.services import analyze_career_goal_with_ai

def match_target_career(goal_text):
    if not goal_text:
        return 'Backend Developer'
    text = goal_text.lower()
    if any(k in text for k in ['backend', 'java', 'spring', 'django server', 'node backend', 'api developer', 'server-side']):
        return 'Backend Developer'
    elif any(k in text for k in ['frontend', 'react', 'vue', 'ui developer', 'web client', 'css', 'html']):
        return 'Frontend Developer'
    elif any(k in text for k in ['full stack', 'fullstack', 'web developer', 'mern', 'full-stack', 'software engineer']):
        return 'Full Stack Developer'
    elif any(k in text for k in ['data scientist', 'data science', 'analytics', 'statistician', 'data analyst']):
        return 'Data Scientist'
    elif any(k in text for k in ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 'nlp', 'llm']):
        return 'AI/ML Engineer'
    elif any(k in text for k in ['cloud', 'devops', 'aws', 'kubernetes', 'sre', 'infrastructure', 'sysadmin']):
        return 'Cloud Engineer'
    elif any(k in text for k in ['security', 'cyber', 'soc', 'penetration', 'ethical hacker', 'infosec']):
        return 'Cybersecurity Analyst'
    return 'Backend Developer'

def calculate_skill_gaps(user, target_career):
    prof_scores = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3}
    user_skills_map = {us.skill.name.lower(): us for us in UserSkill.objects.filter(user=user).select_related('skill')}
    career_skills = CareerSkill.objects.filter(career=target_career).select_related('skill').order_by('prerequisite_order')
    
    gaps = []
    current_skills_display = []
    
    for cs in career_skills:
        sname = cs.skill.name
        req_score = prof_scores.get(cs.required_level, 2)
        us = user_skills_map.get(sname.lower())
        
        if us:
            curr_score = prof_scores.get(us.proficiency, 1)
            curr_level = us.proficiency
            curr_pct = us.proficiency_percent
        else:
            curr_score = 0
            curr_level = 'None'
            curr_pct = 0

        gap_score = max(0, req_score - curr_score)
        
        if gap_score >= 2 or (gap_score == 1 and cs.importance == 'HIGH'):
            priority = 'HIGH'
        elif gap_score == 1 and cs.importance == 'MEDIUM':
            priority = 'MEDIUM'
        elif gap_score == 1:
            priority = 'LOW'
        else:
            priority = 'ACQUIRED' if curr_score >= req_score else 'LOW'

        if priority in ['HIGH', 'MEDIUM']:
            why_it_matters = (
                f"As a target {target_career.name}, mastering {sname} is vital for {cs.importance.lower()} priority milestones. "
                f"Current level: {curr_level}, required level: {cs.required_level}."
            )
        else:
            why_it_matters = f"You have solid competency in {sname} ({curr_level}), satisfying baseline requirements."

        gaps.append({
            'skill_id': cs.skill.id,
            'skill_name': sname,
            'category': cs.skill.category,
            'current_level': curr_level,
            'current_percent': curr_pct,
            'required_level': cs.required_level,
            'importance': cs.importance,
            'gap_score': gap_score,
            'priority': priority,
            'prerequisite_order': cs.prerequisite_order,
            'why_it_matters': why_it_matters
        })

    for us in user_skills_map.values():
        current_skills_display.append({
            'name': us.skill.name,
            'category': us.skill.category,
            'proficiency': us.proficiency,
            'percent': us.proficiency_percent,
        })

    return {
        'gaps': gaps,
        'current_skills': current_skills_display,
        'high_priority_count': sum(1 for g in gaps if g['priority'] == 'HIGH'),
        'medium_priority_count': sum(1 for g in gaps if g['priority'] == 'MEDIUM'),
        'acquired_count': sum(1 for g in gaps if g['priority'] == 'ACQUIRED'),
    }

def generate_recommendations_for_user(user, force_regenerate=False):
    if not force_regenerate:
        existing_roadmap = Roadmap.objects.filter(user=user).order_by('-created_at').first()
        if existing_roadmap and existing_roadmap.milestones.exists():
            return existing_roadmap

    profile, _ = LearnerProfile.objects.get_or_create(user=user)
    career_name = match_target_career(profile.career_goal)
    career, _ = Career.objects.get_or_create(name=career_name)

    Roadmap.objects.filter(user=user).delete()

    graph_data = CAREER_SKILL_GRAPHS.get(career_name, CAREER_SKILL_GRAPHS['Backend Developer'])
    
    roadmap = Roadmap.objects.create(
        user=user,
        career=career,
        title=f"Personalized Career Roadmap: {career.name}",
        description=f"Tailored learning path calibrated for {profile.experience_level} level studying {profile.weekly_hours} hrs/week with target timeline of {profile.target_timeline}."
    )

    user_skills = {us.skill.name.lower(): us.proficiency for us in UserSkill.objects.filter(user=user).select_related('skill')}
    total_hours = 0

    for m_idx, m_info in enumerate(graph_data['milestones'], start=1):
        milestone = Milestone.objects.create(
            roadmap=roadmap,
            title=m_info['title'],
            description=m_info['description'],
            order=m_idx,
            estimated_hours=m_info['hours']
        )
        total_hours += m_info['hours']

        for t_idx, topic_name in enumerate(m_info['topics'], start=1):
            is_known = False
            for sk_name, prof in user_skills.items():
                if sk_name in topic_name.lower():
                    if prof in ['Intermediate', 'Advanced'] and m_idx == 1:
                        is_known = True

            matched_skill = Skill.objects.filter(name__icontains=topic_name.split()[0]).first()

            baseline_status = "Prior baseline demonstrated" if is_known else "Key competency gap identified"
            why_rec = (
                f"Target role: {career.name}. {baseline_status}. "
                f"Mastering '{topic_name}' is required for Milestone {m_idx} projects."
            )

            RoadmapItem.objects.create(
                milestone=milestone,
                title=topic_name,
                item_type='Topic',
                description=f"Core conceptual and practical fundamentals for {topic_name}.",
                skill=matched_skill,
                estimated_hours=round(m_info['hours'] / len(m_info['topics']), 1),
                order=t_idx,
                status='Completed' if is_known else 'Not Started',
                why_recommended=why_rec
            )

        res = LearningResource.objects.filter(skill__category__in=[career.category, 'Backend', 'Frontend', 'Languages', 'DevOps']).first()
        if res:
            RoadmapItem.objects.create(
                milestone=milestone,
                title=f"Curated Resource: {res.title}",
                item_type='Resource',
                description=f"{res.description[:180]}...",
                resource=res,
                skill=res.skill,
                estimated_hours=res.estimated_hours,
                order=len(m_info['topics']) + 1,
                status='Not Started',
                why_recommended=f"Selected from verified platform ({res.platform}) to match your '{profile.learning_style}' learning preference."
            )

        proj = Project.objects.filter(difficulty__in=['Beginner', 'Intermediate'] if m_idx <= 2 else ['Intermediate', 'Advanced']).order_by('?').first()
        if proj:
            RoadmapItem.objects.create(
                milestone=milestone,
                title=f"Milestone Project: {proj.title}",
                item_type='Project',
                description=proj.description,
                project=proj,
                estimated_hours=proj.estimated_hours,
                order=len(m_info['topics']) + 2,
                status='Not Started',
                why_recommended=f"Portfolio project designed to validate your Milestone {m_idx} mastery."
            )

        assess = Assessment.objects.filter(milestone=milestone).first()
        if not assess:
            assess = Assessment.objects.create(
                milestone=milestone,
                title=f"Milestone {m_idx} Competency Assessment",
                description=f"Evaluate your practical grasp of concepts learned in Milestone {m_idx}."
            )
        RoadmapItem.objects.create(
            milestone=milestone,
            title=assess.title,
            item_type='Assessment',
            description=assess.description,
            estimated_hours=0.5,
            order=len(m_info['topics']) + 3,
            status='Not Started',
            why_recommended="Milestone checkpoint quiz to verify concept retention and unlock advanced modules."
        )

    roadmap.total_estimated_hours = total_hours
    roadmap.save()
    return roadmap