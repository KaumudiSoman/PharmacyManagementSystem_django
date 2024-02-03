from rest_framework import serializers
from .models import *
from inventory.models import Inventory

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = '__all__'


class MedLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineLines
        fields = '__all__'


class MedicineLinesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineLines
        fields = ['medicine_id', 'quantity', 'order']

    def create(self, validated_data):
        medicine_id = validated_data.get('medicine_id')
        quantity = validated_data.get('quantity')
        order = validated_data.get('order')
        
        branch = order.order_to  
        
        try:
            inventory = Inventory.objects.get(branch=branch, medicine_id=medicine_id)
            if inventory.quantity < quantity:
                raise serializers.ValidationError(f"Quantity of medicine {medicine_id} is not enough")
        except Inventory.DoesNotExist:
            raise serializers.ValidationError(f'Medicine with {medicine_id} is out of stock')
        
        inventory.quantity -= quantity
        inventory.save()
        
        return MedicineLines.objects.create(medicine_id=medicine_id, quantity=quantity, order=order)

    
class SalesOrderSerializer(serializers.ModelSerializer):
    order_from = serializers.UUIDField()
    order_to = serializers.UUIDField()
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
            order_to = Branch.objects.get(branch_id=order_to_id)
        except Branch.DoesNotExist:
            raise serializers.ValidationError(f'Branch with name {order_to_id} does not exist')
        
        if order_from.role != 'customer':
            raise serializers.ValidationError(f'User with Id {order_from} is not a customer')
        
        validated_data['order_from_id'] = order_from_id
        validated_data['order_to_id'] = order_to.branch_id

        return Orders.objects.create(order_from=order_from, order_to=order_to, type=type)

        # for line_data in medicine_lines_data:
        #     serializer = MedicineLinesSerializer(data=line_data)
        #     serializer.is_valid(raise_exception=True)
        #     serializer.save(order=order)

        # return order

        # for line_data in medicine_lines_data:
        #     line_data['order'] = order.order_id
        #     MedicineLines.objects.create(order=order, **line_data)

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
    