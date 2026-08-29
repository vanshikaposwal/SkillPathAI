from learners.models import LearnerProfile
from roadmap.models import Roadmap

def demo_context(request):
    context = {}
    if request.user.is_authenticated:
        try:
            profile = LearnerProfile.objects.filter(user=request.user).first()
            context['user_profile'] = profile
            roadmap = Roadmap.objects.filter(user=request.user).order_by('-created_at').first()
            context['active_roadmap'] = roadmap
        except Exception:
            pass
    return context
