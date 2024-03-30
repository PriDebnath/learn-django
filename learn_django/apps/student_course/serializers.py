
from rest_framework import serializers
from learn_django.apps.course.models import Course
from learn_django.apps.student.models import Student
from learn_django.apps.student_course.models import StudentCourse

class StudentCourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentCourse
        fields = "__all__"

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')

        # Check if the course is already assigned to this student
        if StudentCourse.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("This course is already assigned to the student")

        return data
