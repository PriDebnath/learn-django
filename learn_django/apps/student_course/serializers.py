
from rest_framework import serializers
from learn_django.apps.course.models import Course
from learn_django.apps.course.serializers import CourseModelSerializer
from learn_django.apps.student.serializers import StudentSerializer
from learn_django.apps.student.models import Student
from learn_django.apps.student_course.models import StudentCourse

class StudentCourseListSerializer(serializers.ModelSerializer):
    "show course list a student"
    course =  CourseModelSerializer()
   
    class Meta:
        model = StudentCourse
        fields = "__all__"
   
     

class CourseStudentListSerializer(serializers.ModelSerializer):
    "show student list a course"
    student =  StudentSerializer()
   
    class Meta:
        model = StudentCourse
        fields = "__all__"
        
        
'''        
  #  def get_course_detail(self, obj):
   #   course_detail = CourseModelSerializer(obj.course)
      return course_detail.data

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')

        # Check if the course is already assigned to this student # we can set the validation at model level as well before saving an instance
        if StudentCourse.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("This course is already assigned to the student")

        return data
'''

class StudentCourseCreateSerializer(serializers.ModelSerializer):
    "create student course"
    class Meta:
        model = StudentCourse
        fields = "__all__"
       
  #  def get_course_detail(self, obj):
   #   course_detail = CourseModelSerializer(obj.course)
    #  return course_detail.data

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')

        # Check if the course is already assigned to this student # we can set the validation at model level as well before saving an instance
        if StudentCourse.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("This course is already assigned to the student")

        return data


class StudentCourseSerializer(serializers.ModelSerializer):
    "perform CRUD on tudentt course"
    course_detail = serializers.SerializerMethodField()
    student_detail = serializers.SerializerMethodField()
    
    class Meta:
        model = StudentCourse
        #fields = [ "id", "course", "course_detail"]
        fields =  "__all__"
       
    def get_course_detail(self, obj):
       course_detail = CourseModelSerializer(obj.course)
       return course_detail.data
   
    def get_student_detail(self, obj):
       student_detail = StudentSerializer(obj.student)
       return student_detail.data

    def validate(self, data):
        student = data.get('student')
        course = data.get('course')

        # Check if the course is already assigned to this student # we can set the validation at model level as well before saving an instance
        if StudentCourse.objects.filter(student=student, course=course).exists():
            raise serializers.ValidationError("This course is already assigned to the student")

        return data
