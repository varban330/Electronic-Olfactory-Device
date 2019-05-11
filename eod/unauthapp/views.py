from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from authapp.models import EndUser
from rest_framework_expiring_authtoken import views as rviews
# Create your views here.

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            user = User()
            # cleaned (normalised) data
            user.username = request.data['username']
            user.email = request.data['email']
            pwd = request.data['password']
            user.set_password(pwd)
            user.save()
            euser = EndUser()
            euser.user = user
            euser.is_admin = False
            euser.save()
            string = "Registration Successful"
            code = 200
        except Exception as e:
            string = "Sorry Registration could not be done"
            code = 400
        content = {'message': string}
        return Response(data=content, status = code)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self,request):
        x = rviews.ObtainExpiringAuthToken()
        if x.post(request).status_code == 200:
            token = x.post(request).data["token"]
            username = request.data["username"]
            user = User.objects.get(username = username)
            euser = EndUser.objects.filter(user = user)
            k = euser[0]
            if euser[0].is_admin:
                status = "admin"
            else:
                status = "user"
            code = 200
            content = {'token': token, 'status' : status}
        else:
            content = x.post(request).data
            code = x.post(request).status_code
        return Response(data=content, status = code)
