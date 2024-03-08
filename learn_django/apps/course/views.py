# Create your views here.
import json
from django.views import View
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.forms.models import model_to_dict
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# @drf
from rest_framework.response import Response
from rest_framework import status, viewsets, generics, filters
from learn_django.apps.course.serializers import (
    CourseModelSerializer,
    CourseWithCategorySerializer,
    CourseModelNoValidationSerializer,
)
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


class CourseListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseWithCategorySerializer

#   filter_backends = [filters.SearchFilter]
#   search_fields=['title']

# class CourseViewSet(viewsets.ViewSet):
#   """
#   ViewSet is amazing it automatically understand and
#   generate urls based on methods
#   """

#   def list(self, request):
#     queryset = Course.objects.all()

#     # filtering using query params
#     category_param = request.query_params.get('category')
#     if category_param:
#       queryset = queryset.filter(category=category_param)

#     # query param in nested
#     category_name_param = request.query_params.get('category_name')
#     if category_name_param:
#       queryset = queryset.filter(category__title=category_name_param) # category__title use the double underscore

#     # searching
#     search_param = request.query_params.get('search')
#     if search_param:
#       queryset = queryset.filter(title__icontains = search_param)

#     # ordering
#     order_params = request.query_params.get('order')
#     if order_params:
#       order_fields = order_params.split(",")
#       queryset = queryset.order_by(*order_fields)
#       #http://localhost:8000/course/view-set?order=price,-id

#     # pagination
#     per_page_params = request.query_params.get('perPage', default=2)
#     page_params = request.query_params.get('page', default=1)
#     count = len(queryset)
#     paginator = Paginator(queryset,per_page=per_page_params)
#     try:
#       queryset = paginator.page(number=page_params)
#     except:
#       queryset = []
#     #
#     book_list = BookModelSerializer(queryset,many=True)

#     return Response({
#       "count": count,
#       "results": book_list.data
#     })

#   def retrieve(self, request, pk):
#     return Response({"message": "get single object - using ViewSet"})

#   def post(self, request):
#     book = BookModelSerializer(data=request.data)
#     book.is_valid(raise_exception=True)
#     if book.is_valid():
#       book.save()
#       print("book---")
#       print(book)
#       print("book.data---")
#       print(book.data)
#       return Response(book.data, status=status.HTTP_201_CREATED)
#     return Response(book.errors, status=status.HTTP_400_BAD_REQUEST)


#   def patch(self, request, pk):
#     return Response({"message": "patch - using ViewSet"})

#   def delete(self, request, pk):
#     return Response({"message": "delete - using ViewSet"})


#
# Django Rest Framework  end
