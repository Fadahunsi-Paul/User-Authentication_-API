from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
import random
from django.conf import settings
from datetime import datetime,timedelta
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model

# user=get_user_model()

class Util:
    @staticmethod
    def send_email(data):
        email=EmailMessage(
            subject=data['Subject'],
            body=data['email_body'],
            to=[data['to_email']])
        email.send() 

def user_email(request,user):
    token = RefreshToken.for_user(user).access_token
    current_site = get_current_site(request).domain
    relativeLink = reverse('verify-email')

    absurl='http://'+current_site+relativeLink+"?token="+str(token)
    email_body = 'Hi '+user.email+' Use the link below to verify Your account \n'+absurl
    data = {'email_body':email_body,'to_email':user.email,'Subject':'Verify Your Email'}
    Util.send_email(data)

def generate_six_digit_code():
    random.randint(100000, 999999)

def send_reset_code(user,code):
    subject= "Reset Password Code"
    message= f'Use this code {code} to reset your password'
    email_sender=settings.EMAIL_HOST_USER
    email_reciever=[user.email]
    send_email = [subject, message, email_sender, email_reciever]
    