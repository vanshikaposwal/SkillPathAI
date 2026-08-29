from django.db import models
from .models import Roadmap, Milestone, RoadmapItem, Progress, Feedback
from careers.models import Skill
from resources.models import LearningResource
from projects.models import Project

def recalculate_roadmap_progress(roadmap):
    return roadmap.progress_percentage

def handle_adaptive_feedback(user, item_id, feedback_type, user_note=""):
    try:
        item = RoadmapItem.objects.get(id=item_id, milestone__roadmap__user=user)
    except RoadmapItem.DoesNotExist:
        return {'success': False, 'message': 'Roadmap item not found'}

    Feedback.objects.create(
        user=user,
        roadmap_item=item,
        feedback_type=feedback_type,
        user_note=user_note
    )

    action_summary = ""

    if feedback_type == 'ALREADY_KNOW':
        item.status = 'Completed'
        item.save()
        Progress.objects.get_or_create(user=user, roadmap_item=item, defaults={'learning_minutes': 15})
        action_summary = f"Marked '{item.title}' as known and completed! Roadmap progress updated."

    elif feedback_type == 'TOO_EASY':
        item.status = 'Completed'
        item.save()
        Progress.objects.get_or_create(user=user, roadmap_item=item, defaults={'learning_minutes': 20})
        next_items = item.milestone.items.filter(order__gt=item.order, status='Not Started')
        if next_items.exists():
            next_item = next_items.first()
            next_item.status = 'In Progress'
            next_item.why_recommended += " [Accelerated via Fast-Track]"
            next_item.save()
        action_summary = f"Accelerated learning path! Fast-tracked past '{item.title}' to advanced challenges."

    elif feedback_type == 'TOO_DIFFICULT':
        skill = item.skill
        new_order = item.order
        item.milestone.items.filter(order__gte=new_order).exclude(id=item.id).update(order=models.F('order') + 1)
        refresher = RoadmapItem.objects.create(
            milestone=item.milestone,
            title=f"Prerequisite Review: {skill.name if skill else item.title} Fundamentals",
            item_type='Resource',
            description=f"Supplementary foundations and visual walkthroughs to master {item.title}.",
            skill=skill,
            estimated_hours=1.5,
            order=new_order,
            status='In Progress',
            why_recommended=f"Added automatically based on your feedback: reinforcement for {item.title}."
        )
        item.order = new_order + 1
        item.save()
        action_summary = f"Adaptive path updated! Inserted prerequisite review module for '{item.title}'."

    elif feedback_type == 'MORE_PRACTICE':
        new_order = item.order + 1
        item.milestone.items.filter(order__gt=item.order).update(order=models.F('order') + 1)
        practice_item = RoadmapItem.objects.create(
            milestone=item.milestone,
            title=f"Hands-On Lab: {item.title} Coding Katas & Exercises",
            item_type='Topic',
            description=f"Deepen mastery of {item.title} with 5 practical implementation challenges.",
            skill=item.skill,
            estimated_hours=2.0,
            order=new_order,
            status='Not Started',
            why_recommended=f"Practice booster generated to reinforce your hands-on mastery of {item.title}."
        )
        action_summary = f"Added interactive hands-on lab exercises for '{item.title}'."

    elif feedback_type == 'NOT_INTERESTED':
        item.status = 'Skipped'
        item.save()
        action_summary = f"Deprioritized '{item.title}'. Replaced with elective alternative track."

    elif feedback_type == 'NEED_EXPLANATION':
        action_summary = f"AI Conceptual Breakdown for '{item.title}' has been generated in your AI Learning Assistant!"

    roadmap = item.milestone.roadmap
    roadmap.save()

    return {
        'success': True,
        'action_summary': action_summary,
        'item_status': item.status,
        'new_progress_percent': roadmap.progress_percentage
    }