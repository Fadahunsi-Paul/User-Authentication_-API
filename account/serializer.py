from .models import User
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,validators=[validate_password],required=True)
    password_confirm = serializers.CharField(write_only=True,validators=[validate_password],required=True)

    class Meta:
        model = User
        fields = ['email','password','password_confirm']

class LoginSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True,required=True,validators=[validate_password])
    
    class Meta:
        model = User
        fields = ['email','password'] 

class VerifyEmailSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=1000)

    class Meta:
        model = User
        fields = ['token']