from django.shortcuts import render
from .models import *
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import *
from inventory.serializers import *
from branch.serializers import *
from orders.serializers import *
from rest_framework import status, viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from accounts.permissions import *
from rest_framework.decorators import action

# Create your views here.

# Create sales order
class SalesOrder(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SalesOrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = serializer.save()
                order_from = CustomUser.objects.get(user_id=order.order_from_id)
                order_to = Branch.objects.get(branch_id=order.order_to_id)
                return Response({'message' : f'Order from {order_from} placed at {order_to} successfully'})
            except Exception as e:
                print(f'errors : {e}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Create medicine lines of an order
class SalesMedicineLines(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        print(request.data.get('order_id'))
        order_uuid = uuid.UUID(request.data.get('order_id'))
        medicine_lines_data = request.data.get('medicine_lines')
        print(medicine_lines_data)

        formatted_medicine_lines = []
        for line_data in medicine_lines_data:
            formatted_line_data = {
                'medicine_id': line_data.get('medicine_id'),
                'quantity': line_data.get('quantity'),
                'order': order_uuid
            }
            formatted_medicine_lines.append(formatted_line_data)

        serializer = MedicineLinesSerializer(data=formatted_medicine_lines, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': f'Medicines for {order_uuid} added successfully'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ViewMedicineLines(viewsets.ModelViewSet):
    serializer_class = MedLineSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCashierX]

    @action(detail=False, methods=['get'])
    def check_medlines(self, request):
        order = request.query_params.get('order')
        med_lines = MedicineLines.objects.filter(order=order)
        medicine_lines = [{
            'medicines' : line.medicine_id.medicine_id, 
            'quantity' : line.quantity, 
            'price' : line.price,
            'line_total' : line.line_total} for line in med_lines]
        return Response({'medicine_lines' : medicine_lines})
    # http://127.0.0.1:8000/medlines/check_medlines/?order=116d1f34-fed1-4e56-b7d4-9023888e7046

class ViewUsers(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManagerX]

    @action(detail=False, methods=['get'])
    def check_role(self, request):
        role = request.query_params.get('role')
        user = CustomUser.objects.filter(role=role)
        users = [{'user_id' : i.user_id, 'email' : i.email} for i in user]
        return Response({f'{role}' : users})
    # http://127.0.0.1:8000/users/check_role/?role=customer


# Cashier can only view the customers of the branch that he works for
class CashierViewCustomers(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_classes = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCashierX]

    def list(self, request):
        user = request.user
        user_uuid = user.user_id
        userbranch = CustomUserBranchRelation.objects.get(user=user_uuid)
        branch = userbranch.branch
        users = CustomUserBranchRelation.objects.filter(branch=branch)
        serializer = CustomUserBranchRelationSerializer(users, many=True)
        user_uuids = [item['user'] for item in serializer.data]
        customers = []
        for user_uid in user_uuids:
            customer = CustomUser.objects.get(user_id=user_uid)
            if customer.role == CustomUser.CUSTOMER:
                customers.append(customer)
        final_customers = [{
            'user_id' : i.user_id, 
            'email' : i.email, 
            'name' : i.name, 
            'dob' : i.dob,
            'address' : i.address} for i in customers]
        return Response({'Customers' : final_customers})
    
    
class CRUDMedicine(viewsets.GenericViewSet, 
                     mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManagerX]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class ViewMedicine(viewsets.ModelViewSet):
    queryset = Medicine.objects.all()
    serializer_class = MedicineSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCashierX]
    

class CRUDBranch(viewsets.GenericViewSet, 
                     mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = BranchSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManagerX]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.MEMPLOYEE:
            user_uuid = user.user_id
            userbranch = CustomUserBranchRelation.objects.get(user=user_uuid)
            branch = userbranch.branch
            return Branch.objects.filter(name=branch)
        else:
            return Branch.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class ViewBranch(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCashierX]
    

# Manager can only perform crud on inventory of the branch that he works for
# ----------------PROBLEM WITH CREATE
class CRUDInventory(viewsets.GenericViewSet, 
                     mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = InventorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManagerX]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.MEMPLOYEE:
            user_uuid = user.user_id
            userbranch = CustomUserBranchRelation.objects.get(user=user_uuid)
            branch = userbranch.branch
            print(branch)
            return Inventory.objects.filter(branch=branch)
        else:
            return Inventory.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
class ViewInventory(viewsets.ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCashierX]

    # to check which branches have the medicine
    @action(detail=False, methods=['get'])
    def check_stock(self, request):
        medicine_id = request.query_params.get('medicine_id')
        inventories = Inventory.objects.filter(medicine_id=medicine_id)
        branches = [{'branch' : inventory.branch.name} for inventory in inventories]
        return Response({'branches' : branches})
    # http://127.0.0.1:8000/inventory/check_stock/?medicine_id=4ffefa8b-a35a-4a85-916d-d6cbe02e4337


class CRUDCustomUser(viewsets.GenericViewSet, 
                     mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManagerX]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    

class CRUDOrders(viewsets.GenericViewSet, 
                     mixins.CreateModelMixin, 
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    serializer_class = OrdersSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsManagerX]

    def get_queryset(self):
        user = self.request.user
        if user.role == CustomUser.MEMPLOYEE:
            user_uuid = user.user_id
            userbranch = CustomUserBranchRelation.objects.get(user=user_uuid)
            branch = userbranch.branch
            branch_id = Branch.objects.get(name=branch)
            return Orders.objects.filter(order_to_id=branch_id.branch_id)
        else:
            return Orders.objects.all()

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
    
    
class ViewOrders(viewsets.ModelViewSet):
    queryset = Orders.objects.all()
    serializer_class = OrdersSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsCashierX]

    # to check all the orders placed at a branch
    @action(detail=False, methods=['get'])
    def check_branch(self, request):
        branch_id = request.query_params.get('order_to_id')
        order = Orders.objects.filter(order_to_id=branch_id)
        orders = [{'orders' : i.order_id} for i in order]
        return Response({'orders' : orders})
    # http://127.0.0.1:8000/orders/check_branch/?order_to_id=62ac3dc5-ec77-4532-a595-0a3ee211d8ad

    # to check all the orders placed by a customer
    @action(detail=False, methods=['get'])
    def check_customer(self, request):
        customer = request.query_params.get('order_from_id')
        order = Orders.objects.filter(order_from_id=customer)
        orders = [{'orders' : i.order_id} for i in order]
        return Response({'orders' : orders})
    # http://127.0.0.1:8000/orders/check_customer/?order_from_id=5308a781-c0c0-4301-9df6-b0eccdc4ff19



# class SalesMedicineLines(APIView):
#     authentication_classes = []
#     permission_classes = [AllowAny]
#     def post(self, request):
#             medicine_lines_data = request.data.get('medicine_lines', [])
#             formatted_medicine_lines = []
#             for line_data in medicine_lines_data:
#                 med_uuid = uuid.UUID(line_data.get('medicine_id'))
#                 quantity = line_data.get('quantity')
#                 formatted_line_data = {
#                     "medicine_id": med_uuid,
#                     "quantity": quantity
#                 }
#                 formatted_medicine_lines.append(formatted_line_data)
#             request.data['medicine_lines'] = formatted_medicine_lines
#             print(med_uuid)
            
#             serializer = SalesOrderSerializer(data=request.data)
#             if serializer.is_valid():
#                 try:
#                     order = serializer.save()
#                     order_from = CustomUser.objects.get(user_id=order.order_from_id)
#                     order_to = Branch.objects.get(branch_id=order.order_to_id)
#                     return Response({'message': f'Order from {order_from} placed at {order_to} successfully'})
#                 except Exception as e:
#                     print(f'errors : {e}')
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


#     def post(self, request):
#         print(request.data.get("order_id"))
#         order_data = request.data.copy()
#         medicine_lines_data = order_data.pop('medicine_lines', [])
#         print(medicine_lines_data)

#         serializer = SalesOrderSerializer(data=order_data)
#         if serializer.is_valid():
#             try:
#                 order = serializer.save()
#                 order_uuid = order.order_id

#                 formatted_medicine_lines = []
#                 for line_data in medicine_lines_data:
#                     formatted_line_data = {
#                         "medicine_id": line_data.get("medicine_id"),
#                         "quantity": line_data.get("quantity"),
#                         "order": order_uuid
#                     }
#                     formatted_medicine_lines.append(formatted_line_data)

#                 serializer2 = MedicineLinesSerializer(data=formatted_medicine_lines, many=True)
#                 if serializer2.is_valid():
#                     serializer2.save()
#                     return Response({'message': f'Medicines for {order_uuid} added successfully'}, status=status.HTTP_200_OK)
#                 else:
#                     return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)
#             except Exception as e:
#                 print(f'error : {e}')
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    