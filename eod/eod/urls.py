"""eod URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from rest_framework.authtoken.views import obtain_auth_token
from unauthapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # /register/
    path('register/', views.RegisterView.as_view(), name='register'),
    # /login/
    path('login/', views.LoginView.as_view(), name='login'),
    # /forgot-pwd-request/
    path('forgot-pwd-request/', views.ForgotAPIView.as_view(), name='forgot-pwd-request'),
    # /reset-pwd-request/
    path('reset-pwd-request/', views.ResetPassword.as_view(), name='reset-pwd-request'),
    # Authentication
    path('', include('authapp.urls')),
    # Device App
    path('device/', include('deviceapp.urls')),
    # Complaint App
    path('complaint/', include('complaintapp.urls')),
    # ML App
    path('ml/', include('mlapp.urls')),
]
