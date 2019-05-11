from django.conf.urls import url, include
from django.urls import path
from . import views


urlpatterns = [
    # Index
    path('hello/', views.HelloView.as_view(), name="Hello"),
    # /register-admin/
    path('register-admin/', views.RegisterAdminView.as_view(), name='register-admin'),

]
