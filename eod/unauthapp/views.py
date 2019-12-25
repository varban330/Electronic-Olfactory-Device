import base64
from datetime import datetime
from django.views.generic import View
from django.shortcuts import render
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from authapp.models import EndUser
from rest_framework_expiring_authtoken import views as rviews
from .functions import send_mail, get_secret_number, check_secret_number, email_anonymizer,active_token
# Create your views here.

api_key = '94cea4adae3c452ebd3c2ff10dd54d7c'

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
            x = LoginView()
            content = x.post(request).data
            content["message"] = string
            code = x.post(request).status_code
        except Exception as e:
            string = "Sorry Registration could not be done"
            code = 400
            content = {'message': string}
        return Response(data=content, status = code)


class ForgotAPIView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        try:
            user = User.objects.get(username = request.data["username"])
            if user is None:
                return Response(data={'message': string}, status = 404)
            euser = EndUser.objects.filter(user = user)[0]
            email = user.email
            message = user.username + ":" +get_secret_number(user.username)+":"+str(int(datetime.timestamp(datetime.now())))
            encodedBytes = base64.b64encode(message.encode("utf-8"))
            encoded_message = str(encodedBytes, "utf-8")
            message_string = "Hey "+user.username+",\nThis is your password reset link:\n" +"https://eod-backend.herokuapp.com/reset-pwd/?key=" + encoded_message +"\nRegards\nEOD Team"
            new_email = email_anonymizer(email)
            if send_mail(email, message_string):
                euser.reset_status = True
                euser.save()
                return Response(data={'message': "Mail Sent Successfully", 'email':new_email}, status = 200)
            else:
                return Response(data={'message': "Error Occurred. Try Again Later"}, status = 500)
        except:
            return Response(data={'message': "Some Error Occurred"}, status = 400)


class ResetPassword(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        try:
            if request.META["HTTP_OCP_APIM_SUBSCRIPTION_KEY"] == api_key:
                key = request.data["secret_key"]
                print(key)
                data = base64.b64decode(key)
                data = data.decode("utf-8")
                data = data.split(":")
                user = User.objects.get(username = data[0])
                if user is None or not check_secret_number(data[0],data[1]):
                    return Response(data={'message': "Try Again. Unauthorised"}, status = 401)
                if not active_token(data[2]):
                    return Response(data={'message': "Expired"}, status = 498)
                pwd = request.data['password']
                user.set_password(pwd)
                user.save()
                euser = EndUser.objects.filter(user = user)[0]
                if not euser.reset_status:
                    return Response(data={'message': "Try Again. Unauthorised"}, status = 401)
                euser.reset_status = False
                euser.save()
                return Response(data={'message': "Password Reset Successful"}, status = 200)
            else:
                return Response(data={'message': "You are not authorised to perform this action"}, status = 401)
        except:
            return Response(data={'message': "Error"}, status = 400)


class ResetPwdView(View):
    template_name = 'unauthapp/index.html'
    failed_template_name = 'unauthapp/sorry.html'

    def get(self,request):
        try:
            key = request.GET.get("key")
            data = base64.b64decode(key)
            data = data.decode("utf-8")
            data = data.split(":")
            user = User.objects.get(username = data[0])
            if user is None or not check_secret_number(data[0],data[1]):
                context = {"message":"Try Again. Unauthorised"}
                return render(request, self.failed_template_name,context)
            if not active_token(data[2]):
                context = {"message":"Try Again. Link has Expired"}
                return render(request, self.failed_template_name,context)
            euser = EndUser.objects.filter(user = user)[0]
            if euser.reset_status:
                context = {"key":key}
                return render(request, self.template_name,context)
            else:
                context = {"message":"Try Again. Unauthorised"}
                return render(request, self.failed_template_name,context)
        except:
            context = {"message":"Error Occurred. Contact Support"}
            return render(request, self.failed_template_name,context)


class ThanksView(View):
    template_name = 'unauthapp/thanks.html'

    def get(self,request):
        return render(request, self.template_name)
