from django.shortcuts import render
from learn_django.apps.student_course.models import StudentCourse
from learn_django.apps.student_course.serializers import StudentCourseSerializer
from rest_framework import generics

class StudentCourseListCreateView(generics.ListCreateAPIView):
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
    