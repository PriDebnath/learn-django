from rest_framework import serializers  
#from django.contrib.auth.models import User 
from learn_django.apps.accounts.models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        print("validated_data=>>",validated_data)
        user = CustomUser.objects.create_user(**validated_data)
        print("created user=>>",user)
        return user

