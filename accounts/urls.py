from django.urls import path
from .views import *


urlpatterns = [
    #path('', include(router.urls))
    path('', home, name='home'),
    path('signup/', SignupUser.as_view(), name='user_signup'),
    path('login/', LoginUser.as_view(), name='user_login'),
    path('verification/<str:token>', email_verification, name='email_verification')
]