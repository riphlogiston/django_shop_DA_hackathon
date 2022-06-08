from email import message
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authtoken.models import Token

from .serializers import *
from .models import CustomUser
from apps.cart.models import ShoppingCart

User=get_user_model()

class RegistrationView(APIView):
    def post(self,request):
        serializer=RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            message='''
            You're done!
            '''
        return Response(message)


class ActivationView(APIView):
    def get(self, request, activation_code):
        user=get_object_or_404(User,activation_code=activation_code)
        user.is_active=True
        user.activation_code=''
        user.save()
        ShoppingCart.objects.create(user=user)
        return Response('Your account is successfully activated', status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer
    

class LogoutView(APIView):
    def get(self,request):
        user=request.user
        token=Token.objects.get(user=user)
        token.delete()
        return Response('You are logged out', status=status.HTTP_401_UNAUTHORIZED)


class ForgetPasswordView(APIView):

    def post(self, request):
        data = request.POST
        serializer = ForgetPasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user: CustomUser = User.objects.get(email=email)
        user.set_activation_code()
        new_password=user.activation_code
        user.activation_code=''
        print(new_password)
        user.set_password(new_password)
        user.save()
        user.send_new_password()
        return Response({'message': 'your new password was send to email'}, status=status.HTTP_200_OK)

class ChangePasswordView(APIView):

    def post(self, request):
        data = request.POST
        serializer = ChangePasswordSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        user: CustomUser = User.objects.get(email=email)
        new_password=serializer.validated_data.get('new_password')
        print(new_password)
        user.set_password(new_password)

        user.save()
        return Response({'message': 'your have changed your password'}, status=status.HTTP_200_OK)



