# Career PathFinder (Skill Path AI)🚀
> **From where you are to where you want to be.**
> *AI-Powered Personalized Learning and Career Recommendation SaaS Platform.*

<img width="2848" height="1658" alt="Screenshot 2026-08-29 at 11 20 29 AM" src="https://github.com/user-attachments/assets/5815037b-bcb8-444e-9c4d-8bb0629c2b91" />

---

## 1. Problem Statement
Online learning platforms offer thousands of courses, but self-directed learners frequently struggle with:
- **Direction Paralysis**: Not knowing what skill or tool to learn first.
- **Skill Gap Blindspots**: Inability to identify missing prerequisite foundations versus advanced concepts.
- **Resource Overload**: Difficulty finding curated, high-quality, verified documentation and courses suited to their specific level.
- **Lack of Practical Application**: Uncertainty about what portfolio projects to build to prove job readiness.
- **Static Roadmaps**: Traditional roadmaps never adapt when a learner finds a topic too easy, too difficult, or already known.

---

## 2. Solution
**Career PathFinder** is a personalized career recommendation platform built on a Directed Acyclic Graph (DAG) skill graph architecture, OpenAI integration, and a continuous adaptive learning feedback loop. 

It analyzes a learner's target career ambition, experience level, verified skills, available weekly study time, learning style, and history to generate a **tailored, explainable, milestone-based learning roadmap**.

---

## 3. Core Features

### 🌟 AI Career Planning & Natural Language Parsing
- Input goals naturally (e.g., *"I want to become a Java backend developer building microservices"*).
- Intelligent domain parser extracts career tracks, timeline, and recommended skill paths.

- <img width="2196" height="1376" alt="Screenshot 2026-08-29 at 11 29 58 AM" src="https://github.com/user-attachments/assets/c8830474-792f-4cae-b913-6acfc9605465" />


### 📊 Scientific Skill Gap Analysis
- Computes `Required Proficiency - Current Proficiency` across career skill graphs.
- Prioritizes gaps into **HIGH**, **MEDIUM**, and **ACQUIRED** categories with explicit prerequisite chains and *"Why it matters"* rationales.

- <img width="2738" height="1508" alt="Screenshot 2026-08-29 at 11 23 03 AM" src="https://github.com/user-attachments/assets/a54af5c3-fdf4-4efe-94b2-092d095a48a7" />


### 🗺️ Dynamic Personalized Learning Roadmap
- Multi-milestone timeline with expandable learning topics, curated resources, hands-on portfolio projects, and checkpoint quizzes.

- <img width="2724" height="1490" alt="Screenshot 2026-08-29 at 11 24 33 AM" src="https://github.com/user-attachments/assets/2843068d-c905-4943-abe8-a3ca925e94a8" />

- **Explainable Recommendations**: Every item features a *"Why this recommendation?"* button explaining its specific role in the learner's path.

### ⚡ Adaptive Learning Engine (Continuous Feedback Loop)
- Submit 1-click feedback on any topic:
  - `TOO_EASY`: Accelerates path, marks item complete, skips redundant basics.
  - `TOO_DIFFICULT`: Automatically inserts prerequisite refresher sub-modules.
  - `ALREADY_KNOW`: Instantly marks item completed and recalculates overall progress.
  - `MORE_PRACTICE`: Injects hands-on coding katas and exercise labs.
  - `NOT_INTERESTED`: Deprioritizes item and suggests elective alternatives.
  - `NEED_EXPLANATION`: Triggers AI conceptual breakdown.

### 🤖 Grounded AI Learning Mentor (`/ai-assistant/`)
- Context-aware chatbot injecting active user profile, target role, current gaps, and active roadmap items into system prompt context.
- Fallback intelligence engine ensures full, high-quality answers even without an OpenAI API key.

### 📈 Real-Time Analytics Dashboard
- **Your Next Best Action**: Prominently highlights the highest-priority incomplete topic with estimated duration and rationale.
- **Chart.js Visualizations**: Skill Radar Competency Matrix, Milestone Completion Breakdown, Weekly Study Hours Tracker, and 7-day Streak Counter.

### 📝 Interactive Milestone Assessments
- Real multiple-choice quizzes with instant grading, scoring, detailed explanations, and automatic roadmap milestone unlock triggers.

---

## 4. AI Architecture Pipeline

```
Learner Profile & Goals
        ↓
Target Career Identification (NLP / Heuristic Parser)
        ↓
DAG Career Skill Graph Traversal (Prerequisite Dependency Hierarchy)
        ↓
Current Skill Mapping & Proficiency Scoring (None=0, Beg=1, Int=2, Adv=3)
        ↓
Skill Gap & Priority Calculation (Gap = Required - Current, Weighted by Importance)
        ↓
Milestone & Roadmap Synthesis (Foundations → Core Web → Frameworks → Production)
        ↓
Resource & Portfolio Project Matching (Verified URLs & Starter Guides)
        ↓
Explainable Recommendation Generation ("Why this recommendation?")
        ↓
Personalized Roadmap & Next Best Action
        ↓
Adaptive Feedback Engine (Continuous Path Recalculation)
```

---

## 5. Technology Stack

- **Backend**: Python 3.10+ / Django 5.0 / Django REST Framework (DRF)
- **Database**: SQLite (Default zero-config setup) / MySQL compatible via Django ORM & `.env`
- **Frontend**: Django Templates + HTML5, CSS3, Vanilla JavaScript, Bootstrap 5
- **Visualizations**: Chart.js 4.4+ (Radar, Bar, Doughnut charts)
- **AI Integration**: OpenAI Python SDK (`gpt-4o-mini`) + Offline Deterministic Heuristic Engine
- **Icons & Typography**: Bootstrap Icons, Google Fonts (Inter)

---

## 6. Project Structure

```
career_pathfinder/
├── manage.py
├── requirements.txt
├── .env.example
├── .env
├── README.md
├── career_pathfinder/          # Core Django project settings & routing
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── accounts/                   # Auth, registration, and 1-Click Demo Login
├── learners/                   # LearnerProfile, UserSkill, Onboarding Wizard
├── careers/                    # Career, Skill, CareerSkill models & seed commands
│   └── management/commands/seed_demo.py
├── recommendations/            # DAG Skill Graph, Gap Calculator, Explainability
│   ├── skill_graph.py
│   └── recommendation_engine.py
├── roadmap/                    # Roadmap, Milestone, Item, Progress, Feedback
│   └── services.py             # Adaptive learning engine
├── resources/                  # Verified curated learning resources library
├── projects/                   # Hands-on portfolio projects catalog
├── assessments/                # Checkpoint quizzes, questions & grading engine
├── ai_assistant/               # Context-aware chatbot & offline AI services
├── dashboard/                  # Analytics calculation & Chart.js feeds
├── templates/                  # Django HTML UI Templates
├── static/                     # CSS stylesheets and Vanilla JS scripts
└── data/                       # Curated JSON datasets (career, resources, projects)
```

---

## 7. Installation & Local Setup

### Prerequisites
- Python 3.10 or higher
- Git

### Steps

1. **Clone or Navigate to the Project Directory**:
   ```bash
   cd career_pathfinder
   ```

2. **Create & Activate Virtual Environment**:
   - On Windows (PowerShell):
     ```powershell
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Database Migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Seed Demo Data & Alex Sharma Profile**:
   ```bash
   python manage.py seed_demo
   ```

6. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open your browser and navigate to: **`http://127.0.0.1:8000/`**

---

## 8. Demo Credentials & 1-Click Login

| Role | Username / Email | Password | Pre-loaded Career Track |
|---|---|---|---|
| **Demo User** | `demo` or `demo@careerpathfinder.ai` | `demo12345` | **Java Backend Developer (Alex Sharma)** |
| **Admin Superuser** | `demo` | `demo12345` | Django Admin Access (`/admin/`) |

> 💡 **Hackathon 1-Click Button**: Clicking **"Try Demo"** on the landing page immediately authenticates you into Alex Sharma's pre-configured dashboard with active milestone progress and charts populated.

---

## 9. API Documentation (Django REST Framework)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/auth/register/` | Register new user account |
| `POST` | `/api/auth/login/` | Authenticate user session |
| `GET` | `/api/dashboard/` | Fetch aggregated dashboard stats, radar data, & Next Best Action |
| `POST` | `/api/profile/analyze/` | AI-powered natural language career goal extraction |
| `GET` | `/api/profile/skills/` | Get current user verified skills |
| `GET` | `/api/roadmap/` | Fetch user's active personalized roadmap |
| `POST` | `/api/roadmap/generate/` | Trigger dynamic roadmap regeneration |
| `POST` | `/api/roadmap/item/<id>/complete/` | Mark roadmap topic/project complete via AJAX |
| `POST` | `/api/roadmap/item/<id>/feedback/` | Submit adaptive learning feedback (`TOO_EASY`, `TOO_DIFFICULT`, etc.) |
| `GET` | `/api/roadmap/item/<id>/why/` | Fetch dynamic explainable recommendation rationale |
| `GET` | `/api/skill-gaps/` | Compute required vs current skill gaps & priorities |
| `GET` | `/api/resources/` | Filter curated learning resources by skill/type/cost |
| `GET` | `/api/projects/` | Filter portfolio projects by difficulty and skills |
| `POST` | `/api/assessment/<id>/submit/` | Submit assessment answers, grade, and update roadmap |
| `POST` | `/api/ai/chat/` | Send message to AI mentor with grounded profile context |

---

## 10. 3–5 Minute Hackathon Judging Demo Flow

1. **Landing Page (`/`)**: Show clean SaaS landing page, features, and supported career tracks.
2. **1-Click Demo Login**: Click **"Try Demo"** to immediately access Alex Sharma's dashboard.
3. **Personalized Dashboard (`/dashboard/`)**:
   - Highlight **Your Next Best Action** card (*"RESTful API Design & Best Practices"* - 45 min).
   - Inspect the **Chart.js Skill Radar Matrix** and **Milestone Completion** chart.
4. **Skill Gap Analysis (`/skill-gaps/`)**:
   - Show verified skills (Java, SQL, Git) vs. High Priority Gaps (Spring Boot, JWT Auth, Docker).
   - Inspect *"Why it matters"* personalized explanations.
5. **Personalized Roadmap (`/roadmap/`)**:
   - Milestone 1 (Foundations) is completed.
   - Milestone 2 is active. Click **"Why?"** on an item to showcase the **Explainable AI Modal**.
6. **Adaptive Learning Feedback**:
   - Click **"Feedback"** on an item, choose **"⚡ Too Easy"** or **"🧩 Too Difficult"**.
   - See the toast notification: *"Learning path adapted: Inserted prerequisite review module..."*
7. **Milestone Assessment (`/assessments/`)**:
   - Open *"REST API Architecture Assessment"*, answer 4 questions, submit, and inspect score & instant feedback.
8. **AI Learning Mentor (`/ai-assistant/`)**:
   - Click prompt chips: *"What should I learn today?"* or *"Why do I need Spring Boot?"*
   - Verify the AI references Alex Sharma's actual active milestone and goals.