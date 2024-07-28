from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import viewsets,status,views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.validators import ValidationError
from rest_framework.decorators import action
from django.utils.translation import gettext_lazy as _
from .serializer import RegistrationSerializer,LoginSerializer,VerifyEmailSerializer
from .utils import Util,user_email
import jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.conf import settings


User = get_user_model()

class RegistrationViewSet(viewsets.GenericViewSet):
    serializer_class = RegistrationSerializer

    @action(detail=False,methods=['post'],permission_classes=[AllowAny])
    def register(self,request):
        try:
            email            = request.data.get('email')
            password         = request.data.get('password','').strip()
            password_confirm = request.data.get('password_confirm','').strip()

            if not all([email,password,password_confirm]):
                return Response({'Error':_('All inputs must be provided')},status=status.HTTP_400_BAD_REQUEST)
            if User.objects.filter(email=email).exists():
                return Response({'Error':_('Email Already exists')},status=status.HTTP_400_BAD_REQUEST)
            if password != password_confirm:
                return Response({'Error':_('Password Fields Do not match')},status=status.HTTP_400_BAD_REQUEST)
            
            if email and password:
                user=User.objects.create_user(
                    email=email,
                    password=password
                )
                user.save()
                user_email(request,user)
                return Response({'Message':_('Registration Successful')},status=status.HTTP_201_CREATED)
            else:
                return Response({'Error': _('Password and Email should be Provided')},status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
    
    @action(detail=False,methods=['post'],permission_classes=[AllowAny])
    def logout(self,request):
        logout(request)
        return Response(_('Logout Successful'),status=status.HTTP_200_OK)
    

class LoginViewset(viewsets.GenericViewSet):
    serializer_class = LoginSerializer

    @action(detail=False,methods=['post'],permission_classes=[AllowAny])
    def login(self,request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(self,email=email,password=password)

            if user:
                if user.is_active:
                    login(request,user)
                    return Response({'Message':_('Login Successful')},status=status.HTTP_201_CREATED)
                else:
                    return Response({'Error':_('Account is Inactive')},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'Error':_('Invalid Login Detailed Provided')},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': f'Internal Server Error: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)  
            

    @action(detail=False,methods=['post'],permission_classes=[AllowAny])
    def logout(self,request):
        logout(request)
        return Response({'Message':_('Logout Successful')},status=status.HTTP_200_OK)
    
class VerifyEmailViewSet(viewsets.GenericViewSet):
    serializer_class = VerifyEmailSerializer

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'token', 
                openapi.IN_QUERY, 
                description="The token for email verification", 
                type=openapi.TYPE_STRING
            )
        ])
    @action(methods=['get'],detail=False,)
    def verify(self,request):
        token = request.GET.get('token')

        try:
            email_token =jwt.decode(token,settings.SECRET_KEY)
            user = User.objects.get(id=email_token['user_id'])
            if not user.is_verified:
                user.is_verified=True
                user.save()
            return Response({'email':'User is Successfully activated'},status=status.HTTP_200_OK) 
        except jwt.ExpiredSignatureError as e:
            return Response({'Error':f'Email Activation Expired : {str(e)}'},status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'Error':f'Invalid Token : {str(e)}'},status=status.HTTP_400_BAD_REQUEST)