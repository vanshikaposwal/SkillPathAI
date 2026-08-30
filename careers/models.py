from django.db import models

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('Languages', 'Languages'),
        ('Frontend', 'Frontend'),
        ('Backend', 'Backend'),
        ('Databases', 'Databases'),
        ('DevOps', 'DevOps & Cloud'),
        ('Data & AI', 'Data & AI'),
        ('Security', 'Security'),
        ('Tools', 'Tools & Version Control'),
        ('Fundamentals', 'Computer Science Fundamentals'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Backend')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class Career(models.Model):
    CATEGORY_CHOICES = [
        ('Software Engineering', 'Software Engineering'),
        ('Data & AI', 'Data & AI'),
        ('Cloud & DevOps', 'Cloud & DevOps'),
        ('Cybersecurity', 'Cybersecurity'),
    ]

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='Software Engineering')
    icon = models.CharField(max_length=50, default='bi-laptop', help_text="Bootstrap icon class")
    average_salary = models.CharField(max_length=50, default='$95,000 - $155,000')
    market_demand = models.CharField(max_length=20, default='Very High')

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class CareerSkill(models.Model):
    PROFICIENCY_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    IMPORTANCE_CHOICES = [
        ('HIGH', 'High Priority / Core'),
        ('MEDIUM', 'Medium Priority / Recommended'),
        ('LOW', 'Low Priority / Supplementary'),
    ]

    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='career_skills')
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='skill_careers')
    required_level = models.CharField(max_length=20, choices=PROFICIENCY_CHOICES, default='Intermediate')
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default='HIGH')
    prerequisite_order = models.IntegerField(default=1, help_text="Topological learning order rank")

    class Meta:
        unique_together = ('career', 'skill')
        ordering = ['prerequisite_order', 'id']

    def __str__(self):
        return f"{self.career.name} - {self.skill.name} ({self.required_level})"
