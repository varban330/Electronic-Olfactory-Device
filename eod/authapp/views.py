from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import EndUser

# Create your views here.
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        string = 'Hello, ' + request.user.username + "!"
        content = {'message': string}
        return Response(content)


class RegisterAdminView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,request):
        try:
            x = EndUser.objects.filter(user = request.user)
            if x[0].is_admin:
                user = User()
                user.username = request.data['username']
                user.email = request.data['email']
                pwd = request.data['password']
                user.set_password(pwd)
                user.save()
                euser = EndUser()
                euser.user = user
                euser.is_admin = True
                euser.save()
                string = "Registration Successful"
                code = 200
            else:
                string = "You're not an admin, You can't register another admin"
                code = 401
        except Exception as e:
            string = "Sorry Registration could not be done"
            code = 400
        content = {'message': string}
        return Response(data=content, status = code)
