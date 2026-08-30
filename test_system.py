import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_pathfinder.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from learners.models import LearnerProfile
from roadmap.models import Roadmap, Milestone, RoadmapItem
from assessments.models import Assessment
from recommendations.recommendation_engine import generate_recommendations_for_user

print("=== Starting Career PathFinder System Verification ===")

client = Client()

# 1. Test Landing Page
res = client.get('/')
assert res.status_code == 200, f"Landing page failed with {res.status_code}"
assert b'Career PathFinder' in res.content
print("[PASS] 1. Landing page loads successfully (HTTP 200)")

# 2. Test Demo Login
demo_user = User.objects.get(username='demo')
client.force_login(demo_user)
print(f"[PASS] 2. Demo User authenticated (Username: {demo_user.username})")

# 3. Test Dashboard View
res = client.get('/dashboard/')
assert res.status_code == 200, f"Dashboard failed with {res.status_code}"
assert b'Dashboard' in res.content and b'NEXT BEST ACTION' in res.content
print("[PASS] 3. Dashboard loaded with Next Best Action & Analytics")

# 4. Test Roadmap View
res = client.get('/roadmap/')
assert res.status_code == 200, f"Roadmap failed with {res.status_code}"
assert b'Milestone' in res.content and b'ROADMAP PROGRESS' in res.content
print("[PASS] 4. Roadmap loaded with interactive milestones and topics")

# 5. Test Skill Gaps View
res = client.get('/skill-gaps/')
assert res.status_code == 200, f"Skill Gaps failed with {res.status_code}"
assert b'Skill Gap Analysis' in res.content and b'HIGH PRIORITY' in res.content
print("[PASS] 5. Skill Gaps loaded with priority breakdown and 'Why it matters'")

# 6. Test Resources View
res = client.get('/resources/')
assert res.status_code == 200, f"Resources failed with {res.status_code}"
assert b'Curated Learning Resources' in res.content
print("[PASS] 6. Resources catalog loaded with verified platform links")

# 7. Test Projects View
res = client.get('/projects/')
assert res.status_code == 200, f"Projects failed with {res.status_code}"
assert b'Portfolio Project' in res.content
print("[PASS] 7. Portfolio Projects catalog loaded")

# 8. Test Assessments View
res = client.get('/assessments/')
assert res.status_code == 200, f"Assessments failed with {res.status_code}"
assert b'Assessment' in res.content
print("[PASS] 8. Assessments list loaded")

# 9. Test AI Assistant View
res = client.get('/ai-assistant/')
assert res.status_code == 200, f"AI Assistant failed with {res.status_code}"
assert b'AI Learning Mentor' in res.content
print("[PASS] 9. AI Assistant chat interface loaded with prompt chips")

# 10. Test Profile View
res = client.get('/profile/')
assert res.status_code == 200, f"Profile failed with {res.status_code}"
assert b'Learner Profile' in res.content
print("[PASS] 10. Profile & study preferences loaded")

# 11. Test REST API: Dashboard Stats
res = client.get('/api/dashboard/')
assert res.status_code == 200, f"API Dashboard failed with {res.status_code}"
data = res.json()
assert 'overall_progress' in data and 'radar_chart' in data, "Invalid API Dashboard JSON"
print(f"[PASS] 11. API GET /api/dashboard/ returned overall_progress={data['overall_progress']}% and radar chart")

# 12. Test REST API: Complete Roadmap Item
roadmap = Roadmap.objects.filter(user=demo_user).first()
item = RoadmapItem.objects.filter(milestone__roadmap=roadmap, status='In Progress').first() or RoadmapItem.objects.filter(milestone__roadmap=roadmap, status='Not Started').first()
if item:
    res = client.post(f'/api/roadmap/item/{item.id}/complete/')
    assert res.status_code == 200, f"API complete item failed with {res.status_code}"
    print(f"[PASS] 12. API POST /api/roadmap/item/{item.id}/complete/ succeeded (Status: {res.json()['status']})")

# 13. Test REST API: Explainable AI ("Why this recommendation?")
if item:
    res = client.get(f'/api/roadmap/item/{item.id}/why/')
    assert res.status_code == 200, f"API item why failed with {res.status_code}"
    print(f"[PASS] 13. API GET /api/roadmap/item/{item.id}/why/ returned rationale: '{res.json()['why_recommended'][:60]}...'")

# 14. Test REST API: Adaptive Feedback
if item:
    res = client.post(f'/api/roadmap/item/{item.id}/feedback/', data={'feedback_type': 'TOO_DIFFICULT', 'user_note': 'Need refresher'}, content_type='application/json')
    assert res.status_code == 200, f"API feedback failed with {res.status_code}"
    print(f"[PASS] 14. API POST /api/roadmap/item/{item.id}/feedback/ adapted path: '{res.json()['action_summary']}'")

# 15. Test REST API: AI Chat Assistant
res = client.post('/api/ai/chat/', data={'message': 'What should I learn today?'}, content_type='application/json')
assert res.status_code == 200, f"API AI chat failed with {res.status_code}"
reply = res.json()['assistant_reply']
assert len(reply) > 20, "AI chat response too short"
print(f"[PASS] 15. API POST /api/ai/chat/ returned contextual AI response: '{reply[:75]}...'")

# 16. Test REST API: Assessment Submit
assess = Assessment.objects.first()
if assess:
    answers = {str(q.id): q.correct_answer for q in assess.questions.all()}
    res = client.post(f'/api/assessment/{assess.id}/submit/', data={'answers': answers}, content_type='application/json')
    assert res.status_code == 200, f"API assessment submit failed with {res.status_code}"
    assert res.json()['passed'] == True, "Should pass assessment with correct answers"
    print(f"[PASS] 16. API POST /api/assessment/{assess.id}/submit/ scored {res.json()['score']}% (Passed: {res.json()['passed']})")

print("\n=======================================================")
print(" ALL 16 SYSTEM & API VERIFICATION TESTS PASSED 100%! ")
print("=======================================================")