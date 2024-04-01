from rest_framework import status
from rest_framework import generics, filters
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from learn_django.apps.student_course.models import StudentCourse
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from learn_django.apps.student_course.serializers import StudentCourseListSerializer, CourseStudentListSerializer, StudentCourseCreateSerializer,StudentCourseSerializer
from django.db.models import Q

class StudentCourseListView(generics.ListAPIView):
    """ 
    pass student id as student query param 
    to get that student's courses .
    It displays course list of a student
    """
    queryset = StudentCourse.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["student"]
    search_fields = ["course__title"]
    serializer_class = StudentCourseListSerializer
    
    #def get_queryset(self): # This is how you can overide getting queryset method 
    #  return StudentCourse.objects.all()

class CourseStudentListView(generics.ListAPIView):
    """ 
    pass course id as course query param 
    to get that course's students .
    It display student list of a course
    """
    queryset = StudentCourse.objects.all()
    serializer_class = CourseStudentListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["course"]
    search_fields = [
        "student__user__first_name",
        "student__user__last_name",
    ]


class StudentCourseCreateView(generics.CreateAPIView):
    """ 
    create student course
    """
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseCreateSerializer


class SearchMixin:
    search_fields = ()  # Define your search fields in subclasses
   
    def search_text(self, queryset):
        search_query = self.request.GET.get("search", None)
        if search_query and self.search_fields:
            search_conditions = Q()
            for field in self.search_fields:
                search_conditions |= Q(**{f"{field}__icontains": search_query})

            queryset = queryset.filter(search_conditions)
        return queryset

class StudentCourseView(SearchMixin, APIView):
    """ 
    A view to handle all CRUD operations for student courses.
    """
    queryset = StudentCourse.objects.all()
    serializer_class = StudentCourseSerializer
 
    search_fields = [
        "course__title",
        "student__user__first_name",
    ]
    
    def get_queryset(self):
      queryset =  StudentCourse.objects.all()
      queryset = self.search_text(queryset)
      return queryset
      
    def get(self, request, pk=None):  # Retrieve or List
        if pk is not None:
            queryset = self.get_queryset().get(pk=pk) #(id=pk)
            serialized_data = self.serializer_class(queryset)
        else:
            queryset = self.get_queryset() # using class's method
            #queryset = self.filter_queryset(queryset) # using class's method
            serialized_data = self.serializer_class(queryset, many=True) # using class's serializer class
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