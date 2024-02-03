from rest_framework import serializers
from .models import *

class BranchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Branch
        fields = '__all__'

class CustomUserBranchRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserBranchRelation
        fields = '__all__'