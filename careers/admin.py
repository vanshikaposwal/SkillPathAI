from django.contrib import admin
from .models import Skill, Career, CareerSkill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    search_fields = ['name']
    list_filter = ['category']

class CareerSkillInline(admin.TabularInline):
    model = CareerSkill
    extra = 1

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'market_demand']
    search_fields = ['name', 'description']
    list_filter = ['category']
    inlines = [CareerSkillInline]

@admin.register(CareerSkill)
class CareerSkillAdmin(admin.ModelAdmin):
    list_display = ['career', 'skill', 'required_level', 'importance', 'prerequisite_order']
    list_filter = ['career', 'required_level', 'importance']
    search_fields = ['career__name', 'skill__name']
