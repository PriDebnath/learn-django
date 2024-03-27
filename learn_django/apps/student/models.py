from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
# Create your models here.

class Student(models.Model):
    age = models.PositiveIntegerField()
    
    class CurrentYear(models.IntegerChoices):
        YEAR_1 = 1, _("Year 1")
        YEAR_2 = 2, _("Year 2")
        YEAR_3 = 3, _("Year 3")
        YEAR_4 = 4, _("Year 4")
        YEAR_5 = 5, _("Year 5")
        YEAR_6 = 6, _("Year 6")
        YEAR_7 = 7, _("Year 7")
        YEAR_8 = 8, _("Year 8")
    current_year = models.PositiveIntegerField(choices=CurrentYear.choices,null=True,blank=True,verbose_name=_("Current Year"))

    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name="students",
        verbose_name=_("User"),
    )
    ## Method to property
    @property
    def name(self):
        full_name = f"{self.user.first_name} {self.user.last_name}".strip()
        return full_name or "Unknown user"
        
      
    # Overriding save method to implement custom logic 
    def save(self, *args, **kwargs):
      super().save(*args, **kwargs)
   
   
    def __str__(self):
        return f"{self.name} - {self.current_year or 'unknown year'}"# Returned value will represent the model