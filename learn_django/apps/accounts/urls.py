from django.urls import path 
from learn_django.apps.accounts import views
urlpatterns = [
  path("registration", views.UserAPIView.as_view() ),
  path("login", views.UserLoginAPIView.as_view() ),
  path("users", views.UserAPIView.as_view() ),
  path("users/<int:pk>", views.UserAPIView.as_view() ),
]