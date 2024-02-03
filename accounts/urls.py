from django.urls import path
from .views import *
from orders.views import *


urlpatterns = [
    #APIView
    path('', home, name='home'),
    path('signup/', SignupUser.as_view(), name='user_signup'),
    path('login/', LoginUser.as_view(), name='user_login'),
    path('user_branch/', UserBranch.as_view(), name='user_branch'),
    path('salesorder/', SalesOrder.as_view(), name='sales_order'),
    path('salesmedicines/', SalesMedicineLines.as_view(), name='sales_medicine_lines'),
    path('verification/<str:token>', email_verification, name='email_verification'),

    #ViewSets
    path('medicines/', ViewMedicine.as_view({'get': 'list'}), name='view_medicines'),
    path('medicines/<uuid:pk>/', ViewMedicine.as_view({'get': 'retrieve'}), name='view_a_medicine'),
    path('inventory/', ViewInventory.as_view({'get': 'list'}), name='view_inventory'),
    path('inventory/<uuid:pk>/', ViewInventory.as_view({'get': 'retrieve'}), name='view_an_inventory'),
    path('inventory/check_stock/', ViewInventory.as_view({'get': 'check_stock'}), name='view_branch_in_stock'),
    path('branches/', ViewBranch.as_view({'get': 'list'}), name='view_branches'),
    path('branches/<uuid:pk>/', ViewBranch.as_view({'get': 'retrieve'}), name='view_a_branch'),
    path('orders/', ViewOrders.as_view({'get': 'list'}), name='view_orders'),
    path('orders/<uuid:pk>/', ViewOrders.as_view({'get': 'retrieve'}), name='view_a_order'),
    path('orders/check_branch/', ViewOrders.as_view({'get': 'check_branch'}), name='view_orders_at_branch'),
    path('orders/check_customer/', ViewOrders.as_view({'get': 'check_customer'}), name='view_orders_by_customer'),
    path('medlines/check_medlines/', ViewMedicineLines.as_view({'get': 'check_medlines'}), name='view_medlines_of_order'),
    path('users/', ViewUsers.as_view({'get': 'list'}), name='view_users'),
    path('users/<uuid:pk>/', ViewUsers.as_view({'get': 'retrieve'}), name='view_a_user'),
    path('users/check_role/', ViewUsers.as_view({'get': 'check_role'}), name='view_role'),
    path('customers/', CashierViewCustomers.as_view({'get': 'list'}), name='customer-list'),
    path('crudmed/', CRUDMedicine.as_view({'get': 'list', 'post' : 'create'}), name='crud_medicine'),
    path('crudmed/<uuid:pk>/', CRUDMedicine.as_view({'delete': 'destroy', 'put': 'update', 'get': 'retrieve'}), name='crud_medicine'),
    path('crudbranch/', CRUDBranch.as_view({'get': 'list', 'post' : 'create'}), name='crud_branch'),
    path('crudbranch/<uuid:pk>/', CRUDBranch.as_view({'delete': 'destroy', 'put': 'update', 'get': 'retrieve'}), name='crud_branch'),
    path('crudinventory/', CRUDInventory.as_view({'get': 'list', 'post' : 'create'}), name='crud_inventory'),
    path('crudinventory/<uuid:pk>/', CRUDInventory.as_view({'delete': 'destroy', 'put': 'update', 'get': 'retrieve'}), name='crud_inventory'),
    path('crudorders/', CRUDOrders.as_view({'get': 'list', 'post' : 'create'}), name='crud_orders'),
    path('crudorders/<uuid:pk>/', CRUDOrders.as_view({'delete': 'destroy', 'put': 'update', 'get': 'retrieve'}), name='crud_orders')
]