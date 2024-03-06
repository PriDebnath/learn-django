from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from learn_django.apps.course.models import Course


class CourseModelSerializer(serializers.ModelSerializer):
  
  ## Method 1: to make a field unique
  title = serializers.CharField(
    validators=[UniqueValidator(queryset=Course.objects.all())]
  )
  
  ## Method 1: Conditions in the field :
  price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
  old_price = serializers.IntegerField(source='price')
  price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")
  
  ## Method 2 : Conditions in the field : Using validate_field() method # it should be above meta class
  def validate_price(self, value):
   if (value < 2):
     raise serializers.ValidationError("price should be greater than 2")
  
  ## Method 4: Using the validate() method # we can validate multiple fields here
  ## you can not use both method 3 and 4 at same time
  def validate(self,attrs):
    if (attrs['price'] < 4):
      raise serializers.ValidationError("price should be greater than 4")
    return super().validate(attrs)
    
    
  class Meta:
    model = Course 
    fields = [
      'id', 
      'title', 
      'price',
      'old_price',
      'price_after_tax',
    ]
     
    ## Method 4: Using keyword arguments in the Meta class
    extra_kwargs = {
    #  "price": {"min_value": 2}
      "title":{
        "validators": [
          UniqueValidator(
            queryset=Course.objects.all()
          )
        ]
      }
    }
    
  
  def calculate_tax(self, obj):
    return obj.price + 8