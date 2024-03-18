from django.urls import path, include
from learn_django.apps.course import views

CLASS_PREFIX = "cls"
FUNC_PREFIX = "func"
DRF_PREFIX = "drf"

urlpatterns = [
    # Function based
    # path("get-course-list",views.get_course_list) # simplified version
    path(f"{FUNC_PREFIX}/courses", views.get_course_list),
    path(f"{FUNC_PREFIX}/courses/<int:course_id>", views.handle_single_course),
    # Class based
    path(f"{CLASS_PREFIX}/courses", views.CourseListView.as_view()),
    path(f"{CLASS_PREFIX}/courses/<int:course_id>", views.CourseListView.as_view()),
    # Drf
    path(f"{DRF_PREFIX}/courses-api-view", views.get_course_list_api_view),
    path(
        f"{DRF_PREFIX}/courses-model-view-set-no-validate",
        views.CourseModelViewSetNoValidation.as_view({"get": "list", "post": "create"}),
    ),
    path(
        f"{DRF_PREFIX}/courses-list-create-generic",
        views.CourseListCreateGenericAPIView.as_view(),
    ),
    path(
        f"{DRF_PREFIX}/filter-courses-with-q",
        views.CourseModelViewSet.as_view({"get": "list"}),
    ),
    path(
        f"{DRF_PREFIX}/courses-viewset",
        views.CourseViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        f"{DRF_PREFIX}/courses-viewset/<int:pk>",
        views.CourseViewSet.as_view({"get": "retrieve", "patch": "patch"}),
    ),
    # authentication authorization
    path(f"{DRF_PREFIX}/auth-user-view", views.authenticated_user_data),
    #path('get-token', obtain_auth_token),
    path(f"{DRF_PREFIX}/student-user-view", views.student_user_view),
    path(f"{DRF_PREFIX}/check-throttle", views.check_throttle),
]
