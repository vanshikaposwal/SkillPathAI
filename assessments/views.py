from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assessment, Question, AssessmentAttempt
from roadmap.models import RoadmapItem, Progress

@login_required
def assessment_list_view(request):
    assessments = Assessment.objects.prefetch_related('questions').all()
    user_attempts = {att.assessment_id: att for att in AssessmentAttempt.objects.filter(user=request.user)}
    return render(request, 'assessments/assessment_list.html', {
        'assessments': assessments,
        'user_attempts': user_attempts,
    })

@login_required
def assessment_take_view(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    questions = assessment.questions.all()
    
    if request.method == 'POST':
        total = questions.count()
        correct_count = 0
        results = []
        
        for q in questions:
            user_ans = request.POST.get(f'q_{q.id}')
            is_correct = (user_ans == q.correct_answer)
            if is_correct:
                correct_count += 1
            results.append({
                'question': q,
                'user_answer': user_ans,
                'is_correct': is_correct,
            })
            
        score = int((correct_count / total * 100)) if total > 0 else 100
        passed = score >= assessment.passing_score
        
        attempt = AssessmentAttempt.objects.create(
            user=request.user,
            assessment=assessment,
            score=score,
            passed=passed
        )
        
        if assessment.milestone:
            item = RoadmapItem.objects.filter(
                milestone=assessment.milestone,
                item_type='Assessment'
            ).first()
            if item:
                item.status = 'Completed'
                item.save()
                Progress.objects.get_or_create(user=request.user, roadmap_item=item)

        return render(request, 'assessments/result.html', {
            'assessment': assessment,
            'attempt': attempt,
            'score': score,
            'passed': passed,
            'results': results,
            'correct_count': correct_count,
            'total': total,
        })
        
    return render(request, 'assessments/assessment.html', {
        'assessment': assessment,
        'questions': questions,
    })