from django.shortcuts import render
from rest_framework import viewsets
from .models import Skill, Career, CareerSkill
from .serializers import SkillSerializer, CareerSerializer, CareerSkillSerializer

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class CareerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Career.objects.all()
    serializer_class = CareerSerializer
