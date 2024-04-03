from rest_framework import status
from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from learn_django.apps.accounts import serializers
from learn_django.apps.accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken
from learn_django.apps.accounts.serializers import UserSerializer


 
class UserLoginAPIView(APIView):
    """ 
    Post either username or email with password to get authenticated
    """
    permission_classes = [AllowAny]
    
    def get(self,request):
        return Response({ 
          "error": UserLoginAPIView.__doc__
        })
      
    def post(self, request):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if username or email is provided
        if username:
            user = authenticate(username=username, password=password)
        elif email:
            user = authenticate(email=email, password=password)
        else:
            return Response({'error': 'Please provide username or email'}, status=status.HTTP_400_BAD_REQUEST)
       
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
              'access_token': str(refresh.access_token),
              'refresh_token': str(refresh)
            })
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        
        
        
class UserAPIView(APIView):
    queryset = CustomUser.objects.all()  # Define an empty queryset
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        return self.register_user(request)
        
    def register_user(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk=None):
      old_user_data = get_user_model().objects.get(id=pk)
      new_user_data = request.data
      serializer = UserSerializer(old_user_data, data=new_user_data, partial=True)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      
    def get(self, request, pk= None):
        try:
          if pk: # Show user list if primary key is not present in url
            user = get_user_model().objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
          else: # Show single user if primary key present in url
            users = get_user_model().objects.all()
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)
        except get_user_model().DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request, user_id):
        try:
            user = get_user_model().objects.get(id=user_id)
            user.delete()
            return Response({'message': 'User deleted successfully'})
        except get_user_model().DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
