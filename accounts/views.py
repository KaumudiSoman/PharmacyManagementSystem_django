from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSignUpSerializer
from rest_framework.authtoken.models import Token
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'POST'])
def home(request):
    return Response({'Message' : 'Welcome to Pharmacy Management System'})


class LoginUser(APIView):
    def post(self, request):
        authentication_classes = []
        permission_classes = [AllowAny]

        email = request.data.get('email')
        password = request.data.get('password')

        User = get_user_model()

        authorized_roles = ['employee-cashier', 'employee-salesman', 'employee-manager', 'employee-administrator']

        try:
            user = User.objects.get(email=email, role__in=authorized_roles)
        except User.DoesNotExist:
            return Response({'message': 'User not found/Unauthorized User'}, status=status.HTTP_404_NOT_FOUND)

        if user.check_password(password):
            try:
                token = Token.objects.get(user=user)
            except Token.DoesNotExist:
                return Response({'message' : 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            return Response({
                'token': token.key,
                'user_email': email,
                'user-role': user.role,
                'message': 'User logged in successfully'
            })
        else:
            return Response({'message': 'Invalid Credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class SignupUser(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message' : 'User Registered Successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)