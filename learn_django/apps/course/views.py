# Create your views here.
import json
import logging
from django.views import View
from django.db.models import Q
from django.http import JsonResponse
from learn_django.apps.course.models import CourseCategory
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# @drf
from rest_framework.response import Response
from learn_django.apps.course.serializers import (
    CourseModelSerializer,
    CourseWithCategorySerializer,
    CourseModelNoValidationSerializer,
)
from rest_framework.throttling import AnonRateThrottle
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, generics, filters
from rest_framework.decorators import api_view, permission_classes, throttle_classes


# @models
from learn_django.apps.course.models import Course

#
# Function based view start


@csrf_exempt  # telling Django not to enforce CSRF protection for the view.
def get_course_list(request):

    if request.method == "GET":
        course_list = []
        course_list_query_set = Course.objects.all()
        for course in course_list_query_set:
            course_list.append(
                {
                    "id": course.id,
                    "title": course.title,
                    "desc": course.desc,
                }
            )
        return JsonResponse(course_list, safe=False)

    elif request.method == "POST":
        data = json.loads(request.body)
        new_course = Course.objects.create(
            title=data.get("title"), desc=data.get("desc")
        )
        response_data = {
            "id": new_course.id,
            "title": new_course.title,
            "desc": new_course.desc,
        }
        return JsonResponse(response_data, status=201)


@csrf_exempt
def handle_single_course(request, course_id):

    if request.method == "GET":
        try:
            course_query_set = Course.objects.get(id=course_id)
            response_data = {
                "id": course_query_set.id,
                "title": course_query_set.title,
                "desc": course_query_set.desc,
            }
            return JsonResponse(response_data, safe=False)
        except:
            return JsonResponse(
                {"error": f"Course with id {course_id} not found."}, status=404
            )

    if request.method == "PATCH":
        course_query_set = Course.objects.get(id=course_id)
        data = json.loads(request.body)
        course_query_set.title = data.get(
            "title", course_query_set.title
        )  # dict.get("title", course_query_set.title): This is calling the get method on the dictionary data to retrieve the value associated with the key "title". If the key "title" is present in the data dictionary, the method returns the corresponding value. If the key "title" is not present in the data dictionary, the method returns the default value, which is provided as the second argument. In this case, the default value is course_query_set.title.
        course_query_set.desc = data.get("desc", course_query_set.desc)
        course_query_set.save()

        response_data = model_to_dict(course_query_set)
        return JsonResponse(response_data, status=200)

    if request.method == "DELETE":
        course_query_set = Course.objects.get(id=course_id)
        course_query_set.delete()
        return JsonResponse({}, status=204)


#
# Function based view end


#
# Class based view start
@method_decorator(csrf_exempt, name="dispatch")
class CourseListView(View):

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")

        if course_id is not None:
            # Retrieve details of a specific course
            course = Course.objects.get(id=course_id)
            response_data = {
                "id": course.id,
                "title": course.title,
                "desc": course.desc,
            }
            return JsonResponse(response_data, safe=False)

        else:
            # Retrieve a list of all courses
            course_list = []
            course_list_query_set = Course.objects.all()
            for course in course_list_query_set:
                course_list.append(
                    {
                        "id": course.id,
                        "title": course.title,
                        "desc": course.desc,
                    }
                )
            return JsonResponse(course_list, safe=False)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        new_course = Course.objects.create(
            title=data.get("title"), desc=data.get("desc")
        )
        response_data = {
            "id": new_course.id,
            "title": new_course.title,
            "desc": new_course.desc,
        }
        return JsonResponse(response_data, status=201)

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        course_id = kwargs.get("course_id")
        course_query_set = Course.objects.get(id=course_id)
        # Update fields if present in the request payload
        if "title" in data:
            course_query_set.title = data["title"]
        if "desc" in data:
            course_query_set.desc = data["desc"]

        course_query_set.save()

        response_data = {
            "id": course_query_set.id,
            "title": course_query_set.title,
            "desc": course_query_set.desc,
        }
        return JsonResponse(response_data, status=200)

    def delete(self, request, *args, **kwargs):
        course_id = kwargs.get("course_id")
        course_query_set = Course.objects.get(id=course_id)
        course_query_set.delete()
        return JsonResponse({}, status=204)


#
# Class based view end

#
# Django Rest Framework  start


@api_view(["GET", "POST"])
def get_course_list_api_view(request):
    if request.method == "GET":
        course_list_query_set = Course.objects.all()
        serialized_courses = CourseModelSerializer(course_list_query_set, many=True)
        return Response(serialized_courses.data, status=status.HTTP_200_OK)

    if request.method == "POST":
        book = CourseModelSerializer(data=request.data)
        print(book)
        if book.is_valid(raise_exception=True):
            return Response(request.data)


class CourseModelViewSetNoValidation(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseModelNoValidationSerializer

    def list(
        self, request, *args, **kwargs
    ):  # list method handles get request, when there is no primary key at the end of the url
        queryset = self.get_queryset()  # refering class's queryset
        serializer = self.get_serializer(
            queryset, many=True
        )  # get_serializer is a method provided by the ModelViewSet class.
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):  # handle post request
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        print("can add additional steps before saving the data")
        serializer.save()
        print("saved data =>", serializer.data)


class CourseModelViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    # filtering
    # queryset = queryset.filter(id=1)
    # filtering with Q
    # queryset = queryset.filter(Q(id=1))
    queryset = queryset.filter(
        ~Q(id=1) & Q(id__gt=6)
    )  # get courses whose id is not equal to 1 and greater than 6
    serializer_class = CourseModelSerializer


class CourseListCreateGenericAPIView(
    generics.ListCreateAPIView
):  # @ListCreateAPIView use for getting a list of data or creating
    queryset = Course.objects.all()
    serializer_class = CourseWithCategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["title"]


class CourseViewSet(viewsets.ViewSet):
    """
      This shows how we can set up
    searching, ordering, filtering,
    nested filtering, ordering
    and pagination manually .
    ## filtering using query params ## http://localhost:8000/drf/courses-viewset?categories=1
    ## Nested filtering using query params ## http://localhost:8000/drf/courses-viewset?categories__id=1
    ## searching  ## http://localhost:8000/drf/courses-viewset?search=c%206
    ## ordering  ## http://localhost:8000/course/view-set?order=price,-id
    ## pagination  ## http://localhost:8000/drf/courses-viewset?perPage=3&page=2
    """

    def list(self, request):
        queryset = Course.objects.all()

        ## ordering
        order_params = request.query_params.get("order")
        if order_params:
            order_fields = order_params.split(",")
            queryset = queryset.order_by(*order_fields)

        ## filtering using query params
        categories_param = request.query_params.get("categories")
        if categories_param:
            queryset = queryset.filter(categories=categories_param)

        ## Nested filtering using query params
        categories_id_param = request.query_params.get("categories__id")
        if categories_id_param:
            queryset = queryset.filter(
                categories__id=categories_id_param
            )  # categories__id use the double underscore for nested case

        ## searching
        search_param = request.query_params.get("search")
        if search_param:
            queryset = queryset.filter(title__icontains=search_param)

        ## pagination
        per_page_params = request.query_params.get("perPage", default=3)
        paginator = Paginator(queryset, per_page=per_page_params)
        page_params = request.query_params.get("page", default=1)
        try:
            queryset = paginator.page(number=page_params)
        except PageNotAnInteger:
            queryset = paginator.page(1)
        except EmptyPage:
            queryset = []

        # course_list = CourseModelSerializer(queryset,many=True)
        course_list = CourseWithCategorySerializer(queryset, many=True)

        return Response({"count": paginator.count, "results": course_list.data})


    def retrieve(self, request, pk):
        course_instance = get_object_or_404(Course, id=pk)
        serialized_course = CourseWithCategorySerializer(course_instance)
        return Response(serialized_course.data)


    def create(self, request):
        course = CourseWithCategorySerializer(data=request.data)
        course.is_valid(raise_exception=True)
        if course.is_valid():
            course.save()
            return Response(course.data, status=status.HTTP_201_CREATED)
        return Response(course.errors, status=status.HTTP_400_BAD_REQUEST)


    def patch(self, request, pk):
        instance = Course.objects.get(pk=pk)
        serializer = CourseWithCategorySerializer(instance, data=request.data, partial= True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       


    def delete(self, request, pk):
        course_query_set = Course.objects.get(id=pk)
        course_query_set.delete()
        return Response({"message": "deleted"})


@api_view()
@permission_classes([IsAuthenticated])
def authenticated_user_data (request):
  user =  model_to_dict(request.user)
  return Response({"message": 'Authenticated user data',"user": user})

# @api_view()
# #@permission_classes([IsAuthenticated])
# def manager_view (request):
#   print (request.user)
#   if request.user.groups.filter(name="Manager"). exists():
#     return Response({"message": 'here is secret'})
#   else:
#     return Response({"message":"you are not Manager"})
# @api_view()
# @throttle_classes([AnonRateThrottle])
# def check_throttle (request):
#   return Response({"message": 'here is secret'}) (edited)

#
# Django Rest Framework  end

# mobile changes
