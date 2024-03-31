from django.urls import path, include
from learn_django.apps.student_course import views
urlpatterns = [
  path("",views.StudentCourseView.as_view()),
  path("<int:pk>",views.StudentCourseView.as_view()),
  path("create-student-course",views.StudentCourseCreateView.as_view()),
  path("courses-of-student",views.StudentCourseListView.as_view()),
  path("students-of-course",views.CourseStudentListView.as_view())
]