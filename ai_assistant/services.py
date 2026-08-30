import os
import json
from django.conf import settings
from .models import ChatMessage
from .prompts import build_ai_system_prompt
from learners.models import LearnerProfile, UserSkill
from roadmap.models import Roadmap, Milestone, RoadmapItem

def analyze_career_goal_with_ai(goal_text, experience_level="Intermediate"):
    api_key = getattr(settings, 'OPENAI_API_KEY', '') or os.getenv('OPENAI_API_KEY', '')
    
    text = goal_text.lower()
    if any(k in text for k in ['backend', 'java', 'spring', 'django', 'node', 'server', 'api']):
        career = "Backend Developer"
        skills = ["Java", "SQL & Relational Databases", "Git & GitHub", "HTTP & RESTful APIs", "Spring Boot"]
    elif any(k in text for k in ['frontend', 'react', 'vue', 'ui', 'css', 'javascript']):
        career = "Frontend Developer"
        skills = ["HTML5 & Semantic Markup", "CSS3 & Modern Layouts", "JavaScript (ES6+)", "React / Modern UI Framework"]
    elif any(k in text for k in ['full stack', 'fullstack', 'mern']):
        career = "Full Stack Developer"
        skills = ["HTML5", "CSS3", "JavaScript", "Python", "SQL", "Django / Spring Boot"]
    elif any(k in text for k in ['data', 'analytics', 'statistics', 'pandas']):
        career = "Data Scientist"
        skills = ["Python", "Pandas Data Wrangling", "NumPy", "Statistics", "Machine Learning"]
    elif any(k in text for k in ['ai', 'machine learning', 'ml', 'deep learning', 'llm', 'nlp']):
        career = "AI/ML Engineer"
        skills = ["Python", "PyTorch / Deep Learning", "Machine Learning", "Transformers & LLMs"]
    elif any(k in text for k in ['cloud', 'devops', 'aws', 'kubernetes', 'docker']):
        career = "Cloud Engineer"
        skills = ["Linux & Bash Scripting", "Cloud Fundamentals (AWS)", "Docker & Containerization", "Kubernetes"]
    elif any(k in text for k in ['security', 'cyber', 'soc', 'ethical hacking']):
        career = "Cybersecurity Analyst"
        skills = ["Computer Networking", "Linux & Bash", "Security Fundamentals", "SIEM & Log Analysis"]
    else:
        career = "Backend Developer"
        skills = ["Python", "SQL & Relational Databases", "HTTP & RESTful APIs"]

    fallback_result = {
        "career": career,
        "experience_level": experience_level,
        "recommended_skills": skills,
        "estimated_timeline": "3 months",
        "rationale": f"Analyzed your goal '{goal_text}'. Aligned with the high-demand {career} learning track."
    }

    if not api_key:
        return fallback_result

    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a career analysis engine. Output valid JSON with keys: career, experience_level, recommended_skills (list of strings), estimated_timeline, rationale."},
                {"role": "user", "content": f"Analyze this career goal: '{goal_text}'. Experience: '{experience_level}'."}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return json.loads(response.choices[0].message.content)
    except Exception:
        return fallback_result

def get_ai_assistant_response(user, user_message):
    profile, _ = LearnerProfile.objects.get_or_create(user=user)
    roadmap = Roadmap.objects.filter(user=user).order_by('-created_at').first()
    
    ChatMessage.objects.create(user=user, role='user', message=user_message)

    api_key = getattr(settings, 'OPENAI_API_KEY', '') or os.getenv('OPENAI_API_KEY', '')

    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            system_prompt = build_ai_system_prompt(profile, roadmap, None)
            
            recent_msgs = ChatMessage.objects.filter(user=user).order_by('-timestamp')[:8]
            history = [{"role": m.role, "content": m.message} for m in reversed(recent_msgs)]
            messages = [{"role": "system", "content": system_prompt}] + history
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.7,
                max_tokens=600
            )
            reply = response.choices[0].message.content
            ChatMessage.objects.create(user=user, role='assistant', message=reply)
            return reply
        except Exception:
            pass

    reply = generate_contextual_fallback_response(user, profile, roadmap, user_message)
    ChatMessage.objects.create(user=user, role='assistant', message=reply)
    return reply

def generate_contextual_fallback_response(user, profile, roadmap, message):
    msg = message.lower()
    
    active_m = None
    next_item = None
    if roadmap:
        active_m = roadmap.milestones.filter(items__status__in=['Not Started', 'In Progress']).first()
        if active_m:
            next_item = active_m.items.filter(status__in=['Not Started', 'In Progress']).first()

    if any(k in msg for k in ['what should i learn', 'what next', 'today', 'recommend']):
        if next_item:
            m_title = active_m.title if active_m else "Current Milestone"
            est_mins = int(next_item.estimated_hours * 60)
            why = next_item.why_recommended or "This builds directly on your prerequisite foundations and unlocks your next milestone project."
            return f"### Target Recommended Next Step Today:\n\n**Topic**: **{next_item.title}** ({m_title})\n\n**Estimated Time**: ~{est_mins} minutes\n\n**Why this is your Next Best Action:**\n{why}\n\nAction item: Head over to your [Personalized Roadmap](/roadmap/) and click **Start** on `{next_item.title}`!"
        else:
            return "Outstanding work! You have completed all topics in your current roadmap. Consider taking a milestone assessment or starting an advanced portfolio project!"

    elif any(k in msg for k in ['spring boot', 'why spring']):
        return f"### Why Spring Boot is Crucial for Your {profile.career_goal} Path:\n\n1. **Industry Standard**: Spring Boot powers over 65% of enterprise Java backends and microservices worldwide.\n2. **Production Acceleration**: It eliminates tedious XML boilerplate with convention-over-configuration and auto-configuration.\n3. **Ecosystem Synergy**: Works out-of-the-box with **Spring Data JPA**, **Spring Security (JWT/OAuth2)**, and cloud-native microservices.\n4. **Bridge to Your Portfolio**: Completing the Spring Boot module unlocks your **E-commerce & Microservices Backend API** project!"

    elif any(k in msg for k in ['skip sql', 'can i skip', 'skip database']):
        return f"### Can You Skip SQL?\n\n**Short Answer**: **Not recommended for a {profile.career_goal}.**\n\nHere is why:\n- ORMs (like Hibernate/JPA or Django ORM) generate SQL queries behind the scenes. Without SQL knowledge, debugging N+1 queries or slow joins is impossible.\n- Senior engineers frequently write custom indexing, transactions, and aggregation queries.\n\nAdaptive Tip: If you already know basic SELECT/INSERT statements, mark **SQL Basics** as *Already Know* in your roadmap, and focus directly on **Complex Joins, Indexing, and JPA Transactions**."

    elif any(k in msg for k in ['5 hours', 'few hours', 'busy', 'time']):
        topic = next_item.title if next_item else 'REST API Architecture'
        return f"### Optimal 5-Hour Weekly Sprint for {profile.career_goal}:\n\nWith **5 hours available this week**, here is your high-impact micro-schedule:\n\n- **Day 1 (1.5 hrs)**: Conceptual deep-dive on `{topic}`.\n- **Day 2 (2.0 hrs)**: Hands-on implementation & coding exercises.\n- **Day 3 (1.5 hrs)**: Milestone Checkpoint Quiz & commit your code to GitHub.\n\nConsistency beats binge studying. Small daily iterations keep your 7-day streak intact!"

    elif any(k in msg for k in ['dependency injection', 'ioc', 'inversion of control']):
        return "### Dependency Injection (DI) Explained Simply:\n\n**The Problem**: If Class `Car` creates `new V8Engine()`, it is tightly coupled. You cannot easily test `Car` with a `MockEngine`.\n\n**The Solution (DI)**: Instead of the Car instantiating its own engine, an external Container (like Spring or Django) **injects** the engine via constructor:\n\n```java\n@Service\npublic class OrderService {\n    private final PaymentRepository repository;\n    public OrderService(PaymentRepository repository) {\n        this.repository = repository;\n    }\n}\n```\n\n**Key Benefits**: Testability, Loose Coupling, and Easy Maintenance."

    elif any(k in msg for k in ['project', 'portfolio', 'build']):
        return f"### Recommended Portfolio Projects for {profile.career_goal}:\n\n1. **Employee & Task Management REST API** (Intermediate)\n   - *Skills*: CRUD, REST Design, DTOs, PostgreSQL/MySQL\n2. **Multi-Tenant E-Commerce Backend Service** (Advanced)\n   - *Skills*: Spring Boot / Django, JWT Authentication, JPA Relationships, Payment Webhooks\n3. **Microservices Cloud Gateway with Docker** (Advanced)\n   - *Skills*: Service Discovery, Docker Compose, CI/CD Actions\n\nExplore all details and guides on your [Projects Page](/projects/)!"

    else:
        focus = next_item.title if next_item else 'Active Roadmap Topics'
        return f"### Career PathFinder AI Mentor\n\nBased on your profile as an aspiring **{profile.career_goal}** ({profile.experience_level} level):\n\n- **Current Focus**: {focus}\n- **Study Pace**: {profile.weekly_hours} hours/week ({profile.target_timeline} target)\n\nFeel free to ask me:\n- *'What should I learn today?'*\n- *'Why do I need Spring Boot?'*\n- *'Explain dependency injection with a code example.'*\n- *'How can I optimize my 5-hour study plan this week?'*"