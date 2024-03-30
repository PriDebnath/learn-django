from django.urls import path, include
from learn_django.apps.student_course import views
urlpatterns = [
  path("",views.StudentCourseListCreateView.as_view())
]