from django.conf.urls import url, include
from django.urls import path
from . import views


urlpatterns = [
    # /register-device/
    path('register-dev/', views.RegisterDevice.as_view(), name="register-dev-admin"),
    # /register-device/
    path('register-device/', views.RegisterOwnDevice.as_view(), name="register-dev-user"),
    # /get-list/
    path('get-list/', views.GetDeviceList.as_view(), name="get-list"),
    # /get-status/
    path('get-status/', views.DeviceStatus.as_view(), name="get-status"),
    # /send-status/
    path('send-status/', views.SendDeviceStatus.as_view(), name="send-status"),

]
