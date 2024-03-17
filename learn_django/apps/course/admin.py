# Register your models here.
from django.contrib import admin
from learn_django.apps.course.models import Course, CourseCategory


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "desc"]


admin.site.register(CourseCategory)

