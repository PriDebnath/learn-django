from django.db import models

# Create your models here.

class Student(models.Model):
    name = models.CharField(max_length=200)
    age = models.PositiveIntegerField()

    def __str__(self):
        return self.name  # Returned value will represent the Model
