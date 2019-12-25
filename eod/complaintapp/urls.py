from django.conf.urls import url, include
from django.urls import path
from . import views


urlpatterns = [
    # /register-complaint/
    path('register-complaint/', views.RegisterComplaint.as_view(), name="register-complaint"),
    # /get-list/
    path('get-list/', views.GetComplaints.as_view(), name="get-list"),
    # /resolve/
    path('resolve/', views.ResolveComplaint.as_view(), name="resolve"),

]
