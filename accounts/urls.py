from django.urls import path
from .views import *
from orders.views import *


urlpatterns = [
    #path('', include(router.urls))
    path('', home, name='home'),
    path('signup/', SignupUser.as_view(), name='user_signup'),
    path('login/', LoginUser.as_view(), name='user_login'),
    path('user_branch/', UserBranch.as_view(), name='user_branch'),
    path('salesorder/', SalesOrder.as_view(), name='sales_order'),
    path('salesmedicines/', SalesMedicineLines.as_view(), name='sales_medicine_lines'),
    path('verification/<str:token>', email_verification, name='email_verification')
]