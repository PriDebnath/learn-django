# Create your views here.
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from learn_django.apps.course.models import Course
from django.views.decorators.csrf import csrf_exempt

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
        course_query_set.title = data.get("title", course_query_set.title) # dict.get("title", course_query_set.title): This is calling the get method on the dictionary data to retrieve the value associated with the key "title". If the key "title" is present in the data dictionary, the method returns the corresponding value. If the key "title" is not present in the data dictionary, the method returns the default value, which is provided as the second argument. In this case, the default value is course_query_set.title.
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
