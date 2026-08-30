from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from .services import get_ai_assistant_response
from learners.models import LearnerProfile

@login_required
def assistant_view(request):
    profile, _ = LearnerProfile.objects.get_or_create(user=request.user)
    messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')
    
    if not messages.exists():
        greeting = (
            f"Hello {request.user.first_name or request.user.username}! I am your AI Career Mentor. "
            f"I have analyzed your {profile.career_goal} learning path and skill gaps. "
            f"Ask me anything — from 'What should I learn today?' to deep conceptual questions!"
        )
        ChatMessage.objects.create(user=request.user, role='assistant', message=greeting)
        messages = ChatMessage.objects.filter(user=request.user).order_by('timestamp')

    return render(request, 'ai/assistant.html', {
        'chat_messages': messages,
        'profile': profile,
    })

@login_required
def clear_history_view(request):
    ChatMessage.objects.filter(user=request.user).delete()
    return redirect('ai_assistant')
