from rest_framework import serializers
from learn_django.apps.student.models import Student
from learn_django.apps.accounts.serializers import UserSerializer
from django.contrib.auth.models import User 
from django.contrib.auth import get_user_model 


class StudentSerializer(serializers.ModelSerializer):
  student_name = serializers.SerializerMethodField(method_name="get_student_name")
  user_detail = serializers.SerializerMethodField() # "get_" + field_name become its method_name
  user = serializers.PrimaryKeyRelatedField(queryset=get_user_model().objects.all())

  class Meta:
    model = Student
    fields = ["id", "name", "student_name", "age", "current_year", "user", "user_detail"]
  
  def get_student_name(self, obj):
    student_name = f"{obj.user.first_name} {obj.user.last_name}"
    return student_name or "Unknown"
    
  def get_user_detail(self, obj):
    serializedData =  UserSerializer(obj.user)
    return serializedData.data
    
  # Adding Validations
  def validate(self, data):
        self.validate_unique_user(data['user'])
        return data

  def validate_unique_user(self, user):
        if Student.objects.filter(user=user).exists():
            raise serializers.ValidationError({ "error": "A student with this user already exists."})

    