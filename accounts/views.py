from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSignUpSerializer, CustomUserBranchRelationSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from .models import CustomUser
from django.http import JsonResponse
from django.contrib.auth import authenticate

# Create your views here.

@api_view()
def home(request):
    return Response({'Message' : 'Welcome to Pharmacy Management System'})

# Logging the user in
class LoginUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        authorized_roles = ['employee-cashier', 'employee-salesman', 'employee-manager', 'employee-administrator']

        user = authenticate(request, email=email, password=password, role__in = authorized_roles)

        if user is not None:
            token = Token.objects.get(user=user)

            return Response({
                'token': token.key,
                'email': email,
                'role': user.role,
                'verified' : user.is_verified,
                'message': 'User logged in successfully'
            })
        else:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Registering new user
class SignupUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.get(user=user)
            email_send(user.email, token)
            # user.save()
            return Response({'message' : 'User Registered Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Sending verification email
def email_send(email, token):
    subject = 'Your account needs to be verified'
    message = f'Click on the link to verify your account http://127.0.0.1:8000/verification/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


# Verifying the email
def email_verification(request, token):
    user_token = get_object_or_404(Token, key=token)
    user = user_token.user
    print(user)
    
    user_obj = CustomUser.objects.get(email=user)
    print(user_obj)
    print(user_obj.is_verified)
    if not user_obj.is_verified:
        user_obj.is_verified = True
        user_obj.save()
        print(user_obj)
        return JsonResponse({'message' : 'verified'})
    return JsonResponse({'message' : 'User already verified'})


class UserBranch(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CustomUserBranchRelationSerializer(data=request.data)
        if serializer.is_valid():
            relation = serializer.save()
            return Response({'message' : f'{relation.user} associated to {relation.branch} successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)