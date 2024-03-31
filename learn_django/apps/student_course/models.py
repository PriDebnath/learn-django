from django.db import models
from learn_django.apps.course.models import Course
from learn_django.apps.student.models import Student
from django.core.exceptions import ValidationError
# Create your models here.

class StudentCourse(models.Model):
  student = models.ForeignKey(
    Student, on_delete = models.SET_NULL, null = True, related_name = "student_course"
  )
  course = models.ForeignKey(
    Course, on_delete = models.SET_NULL, null = True, related_name = "student_course"
  )
  
  def save(self, *args, **kwargs):
        # Check if a similar student-course combination already exists # we can set the validation at serializer level as well in validate method
        existing_relationship = StudentCourse.objects.filter(student=self.student, course=self.course).first()
        if existing_relationship:
            # If a similar relationship already exists, raise validation error
            raise ValidationError("Student already has this course")
        super().save(*args, **kwargs)