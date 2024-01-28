from rest_framework import serializers
from .models import CustomUser
from branch.models import Branch, CustomUserBranchRelation
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from orders.models import *
from inventory.models import Inventory

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
    

class MedicineLinesSerializer(serializers.ModelSerializer):
    # medicine = serializers.CharField()
    # quantity = serializers.CharField()

    class Meta:
        model = MedicineLines
        fields = ['medicine_id', 'quantity', 'order']
    
    def create(self, validated_data):
        print('hello')
        print(validated_data)
        medicine_id = validated_data.get('medicine_id')
        medicine_quantity = validated_data.get('quantity')
        print(medicine_id)
        # order = validated_data.get('order')
        order = self.context.get('order')
        print('order', order)
        
        branch = order.order_to
        print('branch', branch)

        try:
            Inventory.objects.get(branch=branch, medicine_id=medicine_id)
        except Inventory.DoesNotExist:
            raise serializers.ValidationError(f'Medicine with {medicine_id} is out of stock')
        
        return MedicineLines.objects.create(medicine_id=medicine_id, quantity=medicine_quantity, order=order)

    

class SalesOrderSerializer(serializers.ModelSerializer):
    order_from = serializers.CharField()
    order_to = serializers.CharField()
    # medicine_lines = MedicineLinesSerializer(many=True)

    class Meta:
        model = Orders
        fields = ['type', 'order_from', 'order_to']

    def create(self, validated_data):
        order_from_id = validated_data.pop('order_from')
        order_to_id = validated_data.pop('order_to')
        type = validated_data.pop('type')
        # medicine_lines_data = validated_data.pop('medicine_lines', [])
        # order_to = None

        try:
            order_from = CustomUser.objects.get(user_id=order_from_id)
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError(f'User with Id {order_from_id} does not exist')
        
        try:
            order_to = Branch.objects.get(name=order_to_id)
        except Branch.DoesNotExist:
            raise serializers.ValidationError(f'Branch with name {order_to_id} does not exist')
        
        if order_from.role != 'customer':
            raise serializers.ValidationError(f'User with Id {order_from} is not a customer')
        
        validated_data['order_from_id'] = order_from_id
        validated_data['order_to_id'] = order_to.branch_id

        return Orders.objects.create(order_from=order_from, order_to=order_to, type=type)

        # for medicine_line_data in medicine_lines_data:
        #     medicine_id = medicine_line_data.get('medicine_id')
        #     quantity = medicine_line_data.get('quantity')

        #     print(f"Trying to get Inventory for medicine_id: {medicine_id}")

        #     try:
        #         medicine = Inventory.objects.get(medicine_id=medicine_id, branch=order_to.branch_id)
        #         MedicineLines.objects.create(order=order, medicine_id=medicine.medicine_id, quantity=quantity)

        #     except Inventory.DoesNotExist:
        #         raise serializers.ValidationError(f'medicine with id {medicine_id} is out of stock')
        
        # return order
    

    
        # medicine_lines = validated_data.get('medicine_lines', [])

        # for line in medicine_lines:
        #     medicine_id = line.get('medicine_id')
        #     medicine_quantity = line.get('quantity')

    
        # print(order_id)
        # try:
        #     order = Orders.objects.get(order_id=order_id)
        # except Orders.DoesNotExist:
        #     raise serializers.ValidationError(f'Order with id {order_id} does not exist')
    
    # order = Orders.objects.get(order_id=order_id)
        # branch = self.context.get('branch')
        # order_to = Orders.objects.get(order_id=order)
        # order_id = order.order_id
    