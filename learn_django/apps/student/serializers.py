from rest_framework import serializers
from learn_django.apps.student.models import Student


class StudentSerializer(serializers.ModelSerializer):
  student_name = serializers.SerializerMethodField(method_name="get_student_name")
 
  class Meta:
    model = Student
    fields = ["id", "name", "student_name", "age", "current_year", "user"]
  
  def get_student_name(self, obj):
    student_name = f"{obj.user.first_name} {obj.user.last_name}"
    return student_name or "Unknown"
    