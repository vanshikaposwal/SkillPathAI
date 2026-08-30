from .recommendation_engine import calculate_skill_gaps, match_target_career
from careers.models import Career
from learners.models import LearnerProfile

def get_user_skill_gaps_data(user):
    profile, _ = LearnerProfile.objects.get_or_create(user=user)
    career_name = match_target_career(profile.career_goal)
    career, _ = Career.objects.get_or_create(name=career_name)
    gap_data = calculate_skill_gaps(user, career)
    gap_data['target_career'] = career.name
    gap_data['career_obj'] = career
    gap_data['profile'] = profile
    return gap_data
