import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from careers.models import Career, Skill, CareerSkill
from learners.models import LearnerProfile, UserSkill
from resources.models import LearningResource
from projects.models import Project
from assessments.models import Assessment, Question, AssessmentAttempt
from roadmap.models import Roadmap, Milestone, RoadmapItem, Progress
from ai_assistant.models import ChatMessage
from recommendations.skill_graph import CAREER_SKILL_GRAPHS

class Command(BaseCommand):
    help = "Seed database with canonical careers, skill graphs, verified resources, projects, assessments, and the Alex Sharma demo profile."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. Seed Skills & Careers
        skills_dict = {}
        for career_name, graph_data in CAREER_SKILL_GRAPHS.items():
            career_obj, _ = Career.objects.get_or_create(
                name=career_name,
                defaults={
                    'category': graph_data.get('category', 'Software Engineering'),
                    'description': graph_data.get('description', ''),
                    'icon': graph_data.get('icon', 'bi-laptop'),
                    'market_demand': 'High',
                }
            )

            for s_data in graph_data['skills']:
                skill_name = s_data['name']
                if skill_name not in skills_dict:
                    skill_obj, _ = Skill.objects.get_or_create(
                        name=skill_name,
                        defaults={
                            'category': s_data.get('category', 'Backend'),
                            'description': f"Core competency in {skill_name} for modern production systems.",
                        }
                    )
                    skills_dict[skill_name] = skill_obj
                else:
                    skill_obj = skills_dict[skill_name]

                CareerSkill.objects.update_or_create(
                    career=career_obj,
                    skill=skill_obj,
                    defaults={
                        'required_level': s_data.get('required_level', 'Intermediate'),
                        'importance': s_data.get('importance', 'HIGH'),
                        'prerequisite_order': s_data.get('order', 1),
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"Seeded {Career.objects.count()} careers and {Skill.objects.count()} skills."))

        # 2. Seed Verified Resources
        resources_data = [
            ("Official Java Documentation & Tutorials", "https://docs.oracle.com/en/java/", "Documentation", "Oracle / Java Docs", "Java", "Beginner", 5.0, "Free", 4.9),
            ("Spring Boot Official Reference Guide", "https://spring.io/guides", "Documentation", "Spring.io", "Spring Boot", "Intermediate", 6.0, "Free", 5.0),
            ("Building a RESTful Web Service with Spring", "https://spring.io/guides/gs/rest-service/", "Article", "Spring.io", "HTTP & RESTful APIs", "Intermediate", 2.0, "Free", 4.8),
            ("freeCodeCamp Spring Boot & Java Microservices", "https://www.freecodecamp.org/news/tag/spring-boot/", "Course", "freeCodeCamp", "Spring Boot", "Intermediate", 8.0, "Free", 4.9),
            ("PostgreSQL Tutorial & SQL Mastery", "https://www.postgresqltutorial.com/", "Documentation", "PostgreSQL Docs", "SQL & Relational Databases", "Beginner", 4.0, "Free", 4.8),
            ("LeetCode Top SQL 50 Study Plan", "https://leetcode.com/studyplan/top-sql-50/", "Practice", "LeetCode", "SQL & Relational Databases", "Intermediate", 10.0, "Free", 4.9),
            ("MDN Web Docs: HTTP Overview & Status Codes", "https://developer.mozilla.org/en-US/docs/Web/HTTP", "Documentation", "MDN Web Docs", "HTTP & RESTful APIs", "Beginner", 3.0, "Free", 5.0),
            ("Git Official Pro Git Book by Scott Chacon", "https://git-scm.com/book/en/v2", "Documentation", "Git SCM", "Git & GitHub", "Beginner", 4.0, "Free", 4.9),
            ("Docker Getting Started Official Guide", "https://docs.docker.com/get-started/", "Documentation", "Docker Docs", "Docker & Containerization", "Intermediate", 3.5, "Free", 4.8),
            ("AWS Cloud Practitioner Essentials", "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/", "Course", "AWS Training", "Cloud Fundamentals (AWS/GCP/Azure)", "Beginner", 6.0, "Free", 4.9),
            ("Official Python 3 Documentation & Tutorial", "https://docs.python.org/3/tutorial/", "Documentation", "Python.org", "Python", "Beginner", 4.0, "Free", 4.9),
            ("NumPy Quickstart & User Guide", "https://numpy.org/doc/stable/user/quickstart.html", "Documentation", "NumPy Docs", "NumPy & Numerical Computing", "Beginner", 3.0, "Free", 4.8),
            ("Pandas 10 Minutes Guide & Exercises", "https://pandas.pydata.org/docs/user_guide/10min.html", "Documentation", "Pandas Docs", "Pandas Data Wrangling", "Beginner", 3.0, "Free", 4.9),
            ("Kaggle Intro to Machine Learning", "https://www.kaggle.com/learn/intro-to-machine-learning", "Course", "Kaggle", "Machine Learning (Scikit-Learn)", "Beginner", 5.0, "Free", 4.9),
            ("PyTorch Official Deep Learning Tutorials", "https://pytorch.org/tutorials/", "Documentation", "PyTorch.org", "PyTorch / Deep Learning", "Intermediate", 8.0, "Free", 4.9),
            ("HuggingFace NLP Course with Transformers", "https://huggingface.co/learn/nlp-course", "Course", "Hugging Face", "NLP & Large Language Models (LLMs)", "Intermediate", 12.0, "Free", 5.0),
            ("MDN JavaScript Guide & Reference", "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "Documentation", "MDN Web Docs", "JavaScript (ES6+)", "Beginner", 6.0, "Free", 5.0),
            ("React Official Documentation & Tutorial", "https://react.dev/learn", "Documentation", "React.dev", "React / Modern UI Framework", "Intermediate", 5.0, "Free", 5.0),
            ("CSS-Tricks Complete Guide to CSS Grid", "https://css-tricks.com/snippets/css/complete-guide-grid/", "Article", "CSS-Tricks", "CSS3 & Modern Layouts (Flex/Grid)", "Beginner", 2.0, "Free", 4.9),
            ("Kubernetes Interactive Basics Tutorial", "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "Documentation", "Kubernetes.io", "Kubernetes (K8s) Cluster Orchestration", "Intermediate", 5.0, "Free", 4.8),
            ("OWASP Top 10 Security Risks Overview", "https://owasp.org/www-project-top-ten/", "Documentation", "OWASP", "Security Fundamentals & Threat Modeling", "Beginner", 3.0, "Free", 5.0),
            ("Wireshark Official User's Guide", "https://www.wireshark.org/docs/wsug_html_chunked/", "Documentation", "Wireshark", "Security Tools (Wireshark, Nmap, Burp Suite)", "Intermediate", 4.0, "Free", 4.7),
        ]

        for title, url, r_type, platform, skill_name, diff, hrs, cost, rating in resources_data:
            skill_obj = Skill.objects.filter(name__icontains=skill_name.split()[0]).first()
            if skill_obj:
                LearningResource.objects.update_or_create(
                    url=url,
                    defaults={
                        'title': title,
                        'description': f"Comprehensive curriculum covering {skill_name} on {platform}.",
                        'resource_type': r_type,
                        'platform': platform,
                        'skill': skill_obj,
                        'difficulty': diff,
                        'estimated_hours': hrs,
                        'free_or_paid': cost,
                        'rating': rating,
                    }
                )

        self.stdout.write(self.style.SUCCESS(f"Seeded {LearningResource.objects.count()} learning resources."))

        # 3. Seed Hands-on Projects
        projects_data = [
            ("Employee & Department Management REST API", "Design and build a multi-endpoint RESTful CRUD API with JPA relational entities, DTO validation, and pagination.", "Beginner", 10, ["Java", "SQL & Relational Databases", "HTTP & RESTful APIs"]),
            ("TaskFlow: Kanban Task Management Microservice", "Develop a real-time task board backend with status state-machine, JWT authentication, and unit tests.", "Intermediate", 15, ["Java", "Spring Boot", "Authentication & JWT/OAuth2"]),
            ("E-Commerce Order & Inventory Backend Service", "Production-grade backend with PostgreSQL integration, Redis caching, transaction rollbacks, and Docker Compose.", "Advanced", 25, ["Spring Boot", "Spring Data JPA & Hibernate", "Docker & Containerization"]),
            ("Interactive Analytics Dashboard with Chart.js & Django", "Modern responsive web app presenting dynamic data visualizations, filterable metric cards, and REST feeds.", "Intermediate", 12, ["JavaScript (ES6+)", "Python", "SQL & Relational Databases"]),
            ("Customer Churn Prediction Pipeline with Scikit-Learn", "End-to-end data science model with exploratory data analysis, hyperparameter tuning, and FastAPI web deployment.", "Intermediate", 16, ["Python", "Pandas Data Wrangling", "Machine Learning (Scikit-Learn)"]),
            ("RAG Document Question-Answering Chatbot", "Build an intelligent semantic search system using PyTorch, HuggingFace embeddings, and ChromaDB vector store.", "Advanced", 20, ["Python", "PyTorch / Deep Learning", "NLP & Large Language Models (LLMs)"]),
            ("Automated CI/CD Cloud Infrastructure with Terraform & AWS", "Provision a secure multi-AZ VPC on AWS with EC2 autoscaling and GitHub Actions automated pipeline.", "Advanced", 18, ["Linux & Bash Scripting", "Cloud Fundamentals (AWS/GCP/Azure)", "Docker & Containerization"]),
            ("Vulnerability Scanner & Network Traffic Analyzer", "Python-based security scanner utilizing Scapy and Nmap APIs to detect open ports and unencrypted credentials.", "Intermediate", 14, ["Computer Networking & DNS", "Security Fundamentals & Threat Modeling"]),
        ]

        for p_title, p_desc, p_diff, p_hrs, p_skills in projects_data:
            proj, _ = Project.objects.update_or_create(
                title=p_title,
                defaults={
                    'description': p_desc,
                    'difficulty': p_diff,
                    'estimated_hours': p_hrs,
                    'prerequisites': f"Foundational knowledge in {', '.join(p_skills)}",
                    'starter_guide': "1. Scaffold project directory and git repository\n2. Configure entity models & database schemas\n3. Implement core business logic\n4. Add comprehensive unit & integration tests",
                }
            )
            for s_name in p_skills:
                s_obj = Skill.objects.filter(name__icontains=s_name.split()[0]).first()
                if s_obj:
                    proj.skills.add(s_obj)

        self.stdout.write(self.style.SUCCESS(f"Seeded {Project.objects.count()} projects."))

        # 4. Seed Assessments & Questions
        assess_java, _ = Assessment.objects.update_or_create(
            title="Java Backend Foundations Assessment",
            defaults={
                'description': "Test your grasp of Java collections, OOP principles, exception handling, and JDBC.",
                'passing_score': 70,
            }
        )
        q_data_java = [
            ("Which Collection class preserves insertion order and allows constant-time positional access?", "HashSet", "ArrayList", "TreeSet", "PriorityQueue", "B", "ArrayList is backed by a dynamic array which provides O(1) indexed access and maintains insertion order."),
            ("What is the primary difference between checked and unchecked exceptions in Java?", "Checked exceptions are subclasses of RuntimeException", "Unchecked exceptions must be declared in a throws clause", "Checked exceptions are verified at compile-time and must be handled", "There is no difference in modern Java", "C", "Checked exceptions inherit from Exception (not RuntimeException) and are enforced by the compiler to be caught or declared."),
            ("Which statement correctly describes the Singleton design pattern in Java?", "Creates a new object instance for every thread", "Ensures a class has only one instance and provides a global access point", "Prevents class inheritance", "Allows dynamic method injection", "B", "Singleton restricts instantiation of a class to a single object, typically implemented via private constructor and static getInstance()."),
            ("In JDBC, why should you use PreparedStatement instead of Statement?", "PreparedStatement prevents SQL injection attacks via parameter binding and precompiles SQL", "PreparedStatement executes on the client only", "Statement is deprecated in Java 17", "PreparedStatement is slower but safer", "A", "PreparedStatement uses parameterized queries that prevent SQL injection and improves performance through query plan caching."),
        ]
        for q_text, a, b, c, d, ans, expl in q_data_java:
            Question.objects.update_or_create(
                assessment=assess_java,
                question=q_text,
                defaults={'option_a': a, 'option_b': b, 'option_c': c, 'option_d': d, 'correct_answer': ans, 'explanation': expl}
            )

        assess_web, _ = Assessment.objects.update_or_create(
            title="REST API Architecture & HTTP Assessment",
            defaults={
                'description': "Evaluate your understanding of HTTP methods, status codes, RESTful constraints, and JSON schemas.",
                'passing_score': 70,
            }
        )
        q_data_web = [
            ("Which HTTP method is idempotent and intended for complete replacement of a resource?", "POST", "GET", "PUT", "PATCH", "C", "PUT is idempotent and replaces the entire target resource with the request payload."),
            ("Which HTTP status code should be returned when a resource is successfully created?", "200 OK", "201 Created", "204 No Content", "202 Accepted", "B", "201 Created indicates the request succeeded and led to the creation of a new resource."),
            ("What does the 'Stateless' constraint in REST architecture mean?", "The server saves client session tokens in memory", "Each request from client to server must contain all information necessary to understand and process the request", "The server must never interact with a database", "The client cannot store cached responses", "B", "Statelessness requires that no client session context is stored on the server between requests."),
            ("Which HTTP header is used by the client to inform the server about the format of data being sent in the body?", "Accept", "Content-Type", "Authorization", "User-Agent", "B", "Content-Type indicates the media type (e.g. application/json) of the entity-body sent to the receiver."),
        ]
        for q_text, a, b, c, d, ans, expl in q_data_web:
            Question.objects.update_or_create(
                assessment=assess_web,
                question=q_text,
                defaults={'option_a': a, 'option_b': b, 'option_c': c, 'option_d': d, 'correct_answer': ans, 'explanation': expl}
            )

        # 5. Create Demo User: Alex Sharma
        demo_user, created = User.objects.get_or_create(
            username='demo',
            defaults={
                'email': 'demo@careerpathfinder.ai',
                'first_name': 'Alex',
                'last_name': 'Sharma',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        demo_user.set_password('demo12345')
        demo_user.save()

        # Learner Profile
        profile, _ = LearnerProfile.objects.update_or_create(
            user=demo_user,
            defaults={
                'career_goal': 'Java Backend Developer',
                'experience_level': 'Intermediate',
                'weekly_hours': '5-10',
                'target_timeline': '3 months',
                'learning_style': 'Mixed',
                'interests': 'High-throughput APIs, Distributed Systems, Microservices with Spring Boot',
                'learning_history': 'Completed Java 101, OOP foundations, SQL Queries, and basic JDBC console apps.',
                'streak_days': 7,
            }
        )

        # Clean demo attempts & chat
        AssessmentAttempt.objects.filter(user=demo_user).delete()
        ChatMessage.objects.filter(user=demo_user).delete()

        # User Skills (Known)
        demo_skills_map = [
            ("Java", "Advanced", 24),
            ("SQL & Relational Databases", "Intermediate", 12),
            ("Git & GitHub", "Intermediate", 10),
            ("HTML5 & Semantic Markup", "Intermediate", 8),
            ("CSS3 & Modern Layouts (Flex/Grid)", "Beginner", 6),
            ("JavaScript (ES6+)", "Beginner", 6),
            ("Data Structures & Algorithms", "Intermediate", 14),
        ]
        for s_name, prof, months in demo_skills_map:
            s_obj = Skill.objects.filter(name__icontains=s_name.split()[0]).first()
            if s_obj:
                UserSkill.objects.update_or_create(
                    user=demo_user,
                    skill=s_obj,
                    defaults={'proficiency': prof, 'experience_months': months}
                )

        # 6. Build Demo User's Realistic Roadmap
        backend_career = Career.objects.get(name='Backend Developer')
        Roadmap.objects.filter(user=demo_user).delete()

        demo_roadmap = Roadmap.objects.create(
            user=demo_user,
            career=backend_career,
            title="Personalized Career Roadmap: Java Backend Developer",
            description="Calibrated specifically for Alex Sharma (Intermediate, 5-10 hrs/wk, 3-month target). Focuses on bridging Spring Boot, REST APIs, Security, and Cloud Deployment.",
            total_estimated_hours=140
        )

        # Milestone 1 (Completed)
        m1 = Milestone.objects.create(
            roadmap=demo_roadmap,
            title="Milestone 1: Backend Foundations & Core Java Mastery",
            description="Master advanced collections, OOP principles, exception handling, and JDBC.",
            order=1,
            estimated_hours=30
        )
        m1_topics = [
            "Advanced Java Collections & Generics",
            "Object-Oriented Design (SOLID Principles)",
            "Data Structures & Algorithmic Efficiency",
            "JDBC Database Connectivity & Connection Pooling"
        ]
        for idx, t in enumerate(m1_topics, start=1):
            item = RoadmapItem.objects.create(
                milestone=m1,
                title=t,
                item_type='Topic',
                description=f"Deep dive into {t}.",
                estimated_hours=4.0,
                order=idx,
                status='Completed',
                why_recommended="Foundational Java mastery confirmed based on your profile history."
            )
            Progress.objects.get_or_create(user=demo_user, roadmap_item=item, defaults={'learning_minutes': 240})

        p1 = Project.objects.filter(title__icontains="Employee").first()
        if p1:
            item_p1 = RoadmapItem.objects.create(
                milestone=m1,
                title=f"Milestone Project: {p1.title}",
                item_type='Project',
                description=p1.description,
                project=p1,
                estimated_hours=p1.estimated_hours,
                order=5,
                status='Completed',
                why_recommended="Validated your core Java and JDBC understanding."
            )
            Progress.objects.get_or_create(user=demo_user, roadmap_item=item_p1, defaults={'learning_minutes': 600})

        item_a1 = RoadmapItem.objects.create(
            milestone=m1,
            title="Java Backend Foundations Assessment",
            item_type='Assessment',
            description="Evaluate core Java and JDBC concepts.",
            estimated_hours=0.5,
            order=6,
            status='Completed',
            why_recommended="Completed with 100% score! Verified core backend competencies."
        )
        AssessmentAttempt.objects.create(user=demo_user, assessment=assess_java, score=100.0, passed=True)

        # Milestone 2 (Active - In Progress)
        m2 = Milestone.objects.create(
            roadmap=demo_roadmap,
            title="Milestone 2: Web Architecture & RESTful APIs",
            description="Learn request-response lifecycles, HTTP methods, JSON data transfer objects (DTO), and API validation.",
            order=2,
            estimated_hours=35
        )
        m2_items = [
            ("HTTP Protocols, Headers & Status Codes", "Completed", "Master status codes (2xx, 4xx, 5xx) and request headers."),
            ("RESTful API Design & Best Practices", "In Progress", "Your Next Best Action: Essential for building scalable microservices and unlocks Spring Boot."),
            ("JSON Serialization & DTO Validation", "Not Started", "Learn Jackson serialization and Jakarta Bean Validation annotations."),
            ("Global Exception Handling in REST APIs", "Not Started", "Implement centralized @ControllerAdvice error responses."),
        ]
        for idx, (t, stat, why) in enumerate(m2_items, start=1):
            item = RoadmapItem.objects.create(
                milestone=m2,
                title=t,
                item_type='Topic',
                description=f"Comprehensive lessons and practice for {t}.",
                estimated_hours=4.0,
                order=idx,
                status=stat,
                why_recommended=why
            )
            if stat == 'Completed':
                Progress.objects.get_or_create(user=demo_user, roadmap_item=item, defaults={'learning_minutes': 180})

        res_m2 = LearningResource.objects.filter(platform__icontains="Spring.io").first()
        if res_m2:
            RoadmapItem.objects.create(
                milestone=m2,
                title=f"Curated Resource: {res_m2.title}",
                item_type='Resource',
                description=res_m2.description,
                resource=res_m2,
                estimated_hours=res_m2.estimated_hours,
                order=5,
                status='In Progress',
                why_recommended="Recommended official Spring.io tutorial matching your reading/mixed style."
            )

        p2 = Project.objects.filter(title__icontains="TaskFlow").first()
        if p2:
            RoadmapItem.objects.create(
                milestone=m2,
                title=f"Milestone Project: {p2.title}",
                item_type='Project',
                description=p2.description,
                project=p2,
                estimated_hours=p2.estimated_hours,
                order=6,
                status='Not Started',
                why_recommended="Practical REST API project to solidify Milestone 2."
            )

        RoadmapItem.objects.create(
            milestone=m2,
            title="REST API Architecture & HTTP Assessment",
            item_type='Assessment',
            description="Evaluate HTTP methods and REST constraints.",
            estimated_hours=0.5,
            order=7,
            status='Not Started',
            why_recommended="Upcoming quiz to unlock Milestone 3 (Spring Boot)."
        )

        # Milestone 3 (Spring Boot)
        m3 = Milestone.objects.create(
            roadmap=demo_roadmap,
            title="Milestone 3: Spring Boot & Framework Engineering",
            description="Build production-grade services utilizing dependency injection, Spring Data JPA, and Hibernate ORM.",
            order=3,
            estimated_hours=40
        )
        m3_topics = [
            ("Spring Boot Core & Dependency Injection (IoC)", "Core framework concepts and bean lifecycles."),
            ("Spring Data JPA Entities & Hibernate Relationships", "One-to-Many, Many-to-Many and query methods."),
            ("Database Migrations with Flyway / Liquibase", "Version-controlled database schema management."),
            ("Spring Security & JWT Authentication", "Stateless authentication filter chain and password encryption."),
        ]
        for idx, (t, desc) in enumerate(m3_topics, start=1):
            RoadmapItem.objects.create(
                milestone=m3,
                title=t,
                item_type='Topic',
                description=desc,
                estimated_hours=6.0,
                order=idx,
                status='Not Started',
                why_recommended="High priority gap identified in your profile analysis."
            )

        # Milestone 4 (Production & Cloud)
        m4 = Milestone.objects.create(
            roadmap=demo_roadmap,
            title="Milestone 4: Production Security, Testing & Cloud Deployment",
            description="Write automated JUnit/Mockito tests, containerize with Docker, and set up CI/CD.",
            order=4,
            estimated_hours=35
        )
        m4_topics = [
            ("Unit & Integration Testing with JUnit 5 & Mockito", "Test service layers, mock repositories, and test REST controllers with MockMvc."),
            ("Docker Containerization & Docker Compose", "Multi-stage builds and container networking for PostgreSQL."),
            ("CI/CD Automation with GitHub Actions", "Automate linting, unit test execution, and image build on push."),
            ("Cloud Deployment & Monitoring (AWS/Render)", "Deploy live API and configure health checks with Spring Boot Actuator."),
        ]
        for idx, (t, desc) in enumerate(m4_topics, start=1):
            RoadmapItem.objects.create(
                milestone=m4,
                title=t,
                item_type='Topic',
                description=desc,
                estimated_hours=5.0,
                order=idx,
                status='Not Started',
                why_recommended="Final milestone required for industry job readiness."
            )

        self.stdout.write(self.style.SUCCESS("Demo User 'demo' (Alex Sharma) and Roadmap seeded successfully!"))
        self.stdout.write(self.style.SUCCESS("All seed operations completed successfully."))