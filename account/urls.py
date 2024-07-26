from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter

from django.urls import re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

...

schema_view = get_schema_view(
   openapi.Info(
      title="USER AUTHENTICATION API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.app.com/policies/terms/",
      contact=openapi.Contact(email="contact@dafa.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
   path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
   path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
   path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   ...
]

router = DefaultRouter()
router.register(r'',RegistrationViewSet,basename='register')
router.register(r'',LoginViewset,basename='login')
# router.register(r'verify',VerifyEmailViewSet,basename='verify')

urlpatterns = [
    path('',include(router.urls)),
    path('verify-email',VerifyEmailViewSet.as_view({'get':'verify'}),name='verify-email')
]
