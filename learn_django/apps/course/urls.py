from django.urls import path, include
from learn_django.apps.course import views

CLASS_PREFIX = "cls"
FUNC_PREFIX = "func"

urlpatterns = [
    # path("get-course-list",views.get_course_list) # simplified version
    path(f"{FUNC_PREFIX}/get-course-list", views.get_course_list),
    path(f"{FUNC_PREFIX}/single-course/<int:course_id>", views.handle_single_course),
    path(f"{CLASS_PREFIX}/courses", views.CourseListView.as_view()),
    path(f"{CLASS_PREFIX}/courses/<int:course_id>", views.CourseListView.as_view()),
]
