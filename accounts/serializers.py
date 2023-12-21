from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserSignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model  = CustomUser
        fields = ['email', 'password', 'name', 'role', 'dob', 'address']
        extra_kwargs = {'password' : {'write_only' : True}}


    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        user =  CustomUser.objects.create_user(email=email, password=password, **validated_data)
        return user