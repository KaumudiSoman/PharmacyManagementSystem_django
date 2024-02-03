from rest_framework import serializers
from .models import CustomUser
from branch.models import Branch, CustomUserBranchRelation
from rest_framework.exceptions import ValidationError

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserSignUpSerializer(serializers.ModelSerializer):

    branch = serializers.CharField()

    class Meta:
        model  = CustomUser
        fields = ['email', 'password', 'name', 'role', 'dob', 'address', 'branch']
        extra_kwargs = {'password' : {'write_only' : True}}


    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        branch_name = validated_data.pop('branch')
        
        user =  CustomUser.objects.create_user(email=email, password=password, **validated_data)

        try:
            branch = Branch.objects.get(name=branch_name)
            CustomUserBranchRelation.objects.create(user=user, branch=branch)

        except Branch.DoesNotExist:
            raise ValidationError(f'Branch with name {branch_name} does not exist')
            
        return user
    

class CustomUserBranchRelationSerializer(serializers.ModelSerializer):
    user = serializers.CharField()
    branch = serializers.CharField()

    class Meta:
        model = CustomUserBranchRelation
        fields = ['user', 'branch']

    def create(self, validated_data):
        email = validated_data['user']
        branch_name = validated_data['branch']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f'User with email {email} does not exist')
        
        try:
            branch = Branch.objects.get(name=branch_name)
        except Branch.DoesNotExist:
            raise serializers.ValidationError(f'Branch with name {branch_name} does not exist')
        
        return CustomUserBranchRelation.objects.create(user=user, branch=branch)
    