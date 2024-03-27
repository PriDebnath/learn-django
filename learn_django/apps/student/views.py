from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics
from learn_django.apps.student.models import Student
from learn_django.apps.student.serializers import StudentSerializer


class StudentListCreateView(generics.ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer