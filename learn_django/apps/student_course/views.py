from rest_framework import generics
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend,OrderingFilter
from rest_framework.filters import OrderingFilter
from learn_django.apps.student_course.models import StudentCourse
from learn_django.apps.student_course.serializers import StudentCourseListSerializer, CourseStudentListSerializer, StudentCourseCreateSerializer,StudentCourseSerializer


class StudentCourseListView(generics.ListAPIView):
    """ 
    pass student id as student query param 
    to get that student's courses .
    It displays course list of a student
    """
    queryset = StudentCourse.objects.all()
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filterset_fields = ["student"]
    serializer_class = StudentCourseListSerializer


class CourseStudentListView(generics.ListAPIView):
    """ 
    pass course id as course query param 
    to get that course's students .
    It display student list of a course
    """
    queryset = StudentCourse.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course"]
    serializer_class = CourseStudentListSerializer


class StudentCourseCreateView(generics.CreateAPIView):
    """ 
    create student course
    """
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseCreateSerializer


class StudentCourseView(APIView):
    """ 
    A view to handle all CRUD operations for student courses.
    """
    serializer_class = StudentCourseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["course", "student"]
    
    def get_queryset(self):
      return StudentCourse.objects.all()
      
    def get(self, request): # List
      queryset = self.get_queryset() # using class's method
      serialized_data = self.serializer_class(queryset, many = True) # using class's serializer class
      return Response(serialized_data.data)
    
    def get(self, request, pk): # Retrive
      queryset = self.get_queryset().get(pk=pk) #(id=pk)
      serialized_data = self.serializer_class(queryset)
      return Response(serialized_data.data)
 
    def post(self, request, pk):
      serializer = self.serializer_class(data = request.data)
      if serializer.valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 
    def patch(self, request, pk):
      instance = self.get_queryset().get(id=pk)
      serializer = self.serializer_class(instance, request.data, partial = True)
      if serializer.valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def delete(self, request, pk):
      instance = self.get_queryset().get(id=pk)
      instance.delete()
      Response(status=status.HTTP_204_NO_CONTENT)