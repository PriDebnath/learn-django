from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=80)
    desc = models.CharField(max_length=80)
    price = models.PositiveIntegerField(default=10, blank=True)

    def __str__(self):
        return self.title  # Returned value will represent the Model


class CourseCategory(models.Model):
    title = models.CharField(max_length=80)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, related_name="categories"
    )
    class Meta:
       verbose_name_plural = "Course Categories" # This will show up in django admin

    def __str__(self):
       course_title = self.course.title if self.course else 'Unknown'
       return f"{self.title} - {course_title}"
