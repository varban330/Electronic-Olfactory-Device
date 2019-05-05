from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response

# Create your views here.
class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        string = 'Hello, ' + request.user.username + "!"
        content = {'message': string}
        return Response(content)

class RegisterView(APIView):

    def post(self, request):
        try:
            user = User()

            # cleaned (normalised) data
            user.username = request.data['username']
            user.email = request.data['email']
            pwd = request.data['password']
            user.set_password(pwd)
            user.save()
            string = "Registration Successful"
        except Exception as e:
            string = "Sorry Registration could not be done"
        content = {'message': string}
        return Response(content)
