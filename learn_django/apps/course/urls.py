from django.urls import path, include
from learn_django.apps.course import views

CLASS_PREFIX = "cls"
FUNC_PREFIX = "func"

urlpatterns = [
    # path("get-course-list",views.get_course_list) # simplified version
    path(f"{FUNC_PREFIX}/get-course-list", views.get_course_list),
    path(f"{FUNC_PREFIX}/single-course/<int:course_id>", views.handle_single_course),
]
