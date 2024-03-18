import logging
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from learn_django.apps.course.models import Course, CourseCategory


class CourseModelSerializer(serializers.ModelSerializer):

    ## Method 1: to make a field unique
    title = serializers.CharField(
        validators=[UniqueValidator(queryset=Course.objects.all())]
    )

    ## Method 1: Conditions in the field :
    price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    old_price = serializers.IntegerField(source="price", required=False)
    price_after_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    ## Method 2 : Conditions in the field : Using validate_field_name() method # it should be above meta class
    def validate_price(self, value):
        if value < 2:
            raise serializers.ValidationError("price should be greater than 2")

    ## Method 3 : Conditions in the field : Using the validate() method # we can validate multiple fields here
    ## you can not use both method 3 and 4 at same time
    def validate(self, attrs):
        if attrs["price"] < 4:
            raise serializers.ValidationError("price should be greater than 4")
        return super().validate(attrs)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "price",
            "old_price",
            "price_after_tax",
        ]

        extra_kwargs = {
            #  "price": {"min_value": 2}  ## Method 4 : Conditions in the field : Using keyword arguments in the Meta class
            "title": {
                "validators": [UniqueValidator(queryset=Course.objects.all())]
            }  ## Method 2: to make a field unique
        }

    def calculate_tax(self, obj):
        return obj.price + 8


class CourseCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)

    class Meta:
        model = CourseCategory
        fields = ["id", "title"]


class CourseModelNoValidationSerializer(serializers.ModelSerializer):
    categories = CourseCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ["id", "title", "categories"]


class CourseWithCategorySerializer(serializers.ModelSerializer):
    categories = CourseCategorySerializer(many=True)  # Nested serializer for categories
    categories_method_field = (
        serializers.SerializerMethodField()
    )  # by default SerializerMethodField is read-only , so it won't apear in validated_data in create method

    """
    ## Method 1:  to get categories of a course :
    Add related_name='categories' to the ForeignKey field in the CourseCategory model.
    This allows you to use # categories = serializers.SerializerMethodField() to access related categories.
    """

    class Meta:
        model = Course
        fields = ["id", "title", "price", "categories", "categories_method_field"]

    def get_categories_method_field(self, obj):
        categories = obj.categories.all()  # using related_name
        # categories = obj.coursecategory_set.all()
        """
            ## Method 2: Explain: categories = obj.coursecategory_set.all() ## In Django,
            when you define a ForeignKey relationship from one model to another,
            Django automatically creates a reverse relation on the related model.
            This reverse relation is named by default as <model_name>_set. In your case,
            since you have a ForeignKey relationship from CourseCategory to Course .
            Django creates a reverse relation on the Course model, and the default name for this relation is
            coursecategory_set. This allows you to access all related CourseCategory objects for a given Course instance.
            This won't work if you already set a related_name.
            """
        return CourseCategorySerializer(categories, many=True).data

    def create(self, validated_data):
        categories_data = validated_data.pop("categories", [])
        course = Course.objects.create(**validated_data)
        # Associate categories with the course
        for category in categories_data:
            category_instance = CourseCategory.objects.get(pk=category["id"])
            course.categories.add(category_instance)
        return course
        
    def update(self, instance, validated_data):
        categories_data = validated_data.pop("categories", [])
      
        #instance = super().update(instance,validated_data) # one liner update
        # Update instance with validated data
        for key, value in validated_data.items():
          setattr(instance, key, value)
        
        # Clear existing categories
        instance.categories.clear()
        
        # Associate categories with the course
        for category_data in categories_data:
            category_instance, created = CourseCategory.objects.get_or_create(**category_data)
            instance.categories.add(category_instance)

        instance.refresh_from_db()
        instance.save
        return instance