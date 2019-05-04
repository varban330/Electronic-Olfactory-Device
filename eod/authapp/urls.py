from django.conf.urls import url, include
from django.urls import path
from . import views
from rest_framework_expiring_authtoken import views as rviews

urlpatterns = [
    # Index
    path('hello/', views.HelloView.as_view(), name="Hello"),
    path('api-token-auth/', rviews.obtain_expiring_auth_token, name='api_token_auth'),
]
