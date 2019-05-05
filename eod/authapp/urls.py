from django.conf.urls import url, include
from django.urls import path
from . import views
from rest_framework_expiring_authtoken import views as rviews

urlpatterns = [
    # Index
    path('hello/', views.HelloView.as_view(), name="Hello"),
    # /get-token/
    path('get-token/', rviews.obtain_expiring_auth_token, name='get_token'),
    # /register/
    path('register/', views.RegisterView.as_view(), name='register'),
]
