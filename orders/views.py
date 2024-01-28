from django.shortcuts import render
from .models import *
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.serializers import *
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect

# Create your views here.


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
    

class SalesMedicineLines(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        order_id = request.data.get('order_id')
        print(order_id)
        
        # medicine_lines_data = request.data.get('medicine_lines', [])
        # for line in medicine_lines_data:
        #     line['order'] = order_id
        # print('data : ', medicine_lines_data)
        print('data : ', request.data)
        order = Orders.objects.get(order_id=order_id)
        print(order.order_date)
        print(order_id)
        serializer = MedicineLinesSerializer(data=request.data, context={'order' : order})
        print(serializer)
        print('1')
        if serializer.is_valid():
            print('5')
            try:
                serializer.save()
                print('2')
                # order_id = Orders.objects.get(order=order_id)
                print('3')
                return Response({'message' : f'Medicines for {order_id} are '})
            except Exception as e:
                print(f'errors : {e}')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def post(self, request):
#         order_data = {
#             'type' : request.data.get('type'),
#             'order_from' : request.data.get('order_from'),
#             'order_to' : request.data.get('order_to')
#         }
#         # medicine_lines_data = request.data.get('medicine_lines', [])

#         medicine_lines_data = request.data.get('medicine_lines', [])

#         serializer1 = SalesOrderSerializer(data=order_data)

#         print(order_data)
#         print(serializer1)
#         print('1')

#         if serializer1.is_valid():
#             print('2')
#             try:
#                 print('3')
#                 order = serializer1.save()
#                 # medicine_lines_data = {
#                 #     'order_to': serializer1.instance.order_to,
#                 #     'medicine_lines': medicine_lines
#                 # }
#                 for line in medicine_lines_data:
#                     line['order'] = order
#                 print(medicine_lines_data)
#                 serializer2 = MedicineLinesSerializer(data=medicine_lines_data, many=True, context={'branch': order.order_to}) #, context={'branch': order.order_to}
#                 print(serializer2)
#                 if serializer2.is_valid():
#                     print('4')
#                     try:
#                         print(order.order_id)
#                         serializer2.save()
#                         print('5')
#                         order_from = CustomUser.objects.get(user_id=order.order_from_id)
#                         order_to = Branch.objects.get(branch_id=order.order_to_id)
#                         return Response({'message' : f'Order from {order_from} placed at {order_to} successfully'})
#                     except Exception as e:
#                         print(f'errors : {e}')
#                 return Response(serializer2.errors, status=status.HTTP_400_BAD_REQUEST)
#             except Exception as e:
#                 print(f'error : {e}')
#         return Response(serializer1.errors, status=status.HTTP_400_BAD_REQUEST)
