from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self,email,password,**extra_fields):
        if not email:
            raise ValueError (_('Provide an email'))
        if len(password)<8:
            raise ValueError(_('Password should be more than 8 characters'))
        if not '@' in email and '.com' in email:
            raise ValueError(_("Email should contain '@' and '.com' "))
        
        user = self.model(email=self.normalize_email(email),**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,password,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        extra_fields.setdefault('is_active',True)

        if extra_fields.get('is_staff') != True:
            raise ValueError(_('Superuser should have is_staff = True'))
        if extra_fields.get('is_superuser') != True:
            raise ValueError(_('Superuser should have is_superuser = True'))
        if extra_fields.get(_('is_active')) != True:
            raise ValueError(_('Superuser should have is_active = True'))
        
        return self.create_user(email,password,**extra_fields)
        
