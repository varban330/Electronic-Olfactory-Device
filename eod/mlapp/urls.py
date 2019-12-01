from django.conf.urls import url, include
from django.urls import path
from . import views

urlpatterns = [
    # /hello-ml/
    path('hello-ml/', views.Helloml.as_view(), name="hello-ml"),

    # /predict-class/
    path('predict-class/', views.PredictSmell.as_view(), name="predict_class")
    ]
