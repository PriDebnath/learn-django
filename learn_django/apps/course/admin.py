# Register your models here.
from django.contrib import admin
from learn_django.apps.course.models import Course


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "desc"]
