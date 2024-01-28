from django.urls import path
from .views import *


urlpatterns = [
    path('salesorder/', SalesOrder.as_view(), name='sales_order'),
]