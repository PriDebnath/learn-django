from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=80)
    desc = models.CharField(max_length=80)

    def __str__(self):
        return self.name  # Returned value will represent the Model
