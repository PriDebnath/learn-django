from django.db import models

# Create your models here.


class Course(models.Model):
    title = models.CharField(max_length=80)
    desc = models.CharField(max_length=80)
    price = models.PositiveIntegerField(default=10, blank=True)

    def __str__(self):
        return self.title  # Returned value will represent the Model
