from django.urls import path, include
from learn_django.apps.student import views

urlpatterns = [
  path("", views.StudentListCreateView.as_view())
]