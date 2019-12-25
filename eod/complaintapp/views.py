from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from deviceapp.models import Device
from rest_framework.views import APIView
from rest_framework.response import Response
from authapp.models import EndUser
from .models import Complaint

COMPLAINT_TYPES = ("device", "app", "other")
# Create your views here.
class RegisterComplaint(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        x = EndUser.objects.filter(user = request.user)[0]
        if x.is_admin:
            message = "You are an Admin, Solve it yourself"
            code = 400
        else:
            complaint_type = request.data["type"]
            if complaint_type in COMPLAINT_TYPES:
                if complaint_type == "device":
                    dev = Device.objects.filter(device_id = request.data["device_id"])[0]
                    complaint = Complaint()
                    complaint.type = complaint_type
                    complaint.user = x
                    complaint.desc = request.data["desc"]
                    complaint.device = dev
                    complaint.save()
                    message = "Device Complaint Registered Successfully"
                    code = 200
                else:
                    complaint = Complaint()
                    complaint.type = complaint_type
                    complaint.user = x
                    complaint.desc = request.data["desc"]
                    complaint.device = None
                    complaint.save()
                    message = "App or Other Complaint Registered Successfully"
                    code = 200
            else:
                message = "Incorrect Complaint Type"
                code = 400
        content = {"message":message}
        return Response(data = content, status = code)


class GetComplaints(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        x = EndUser.objects.filter(user = request.user)[0]
        if x.is_admin:
            data = dict(request.query_params)
            if "type" in data.keys():
                complaints = Complaint.objects.filter(type = data["type"][0])
            else:
                complaints = Complaint.objects.all()
            complaint_list = list()
            for c in complaints:
                if c.type == "device":
                    complaint_list.append({"pk": c.pk, "username": c.user.user.username, "type": c.type, "device_id": c.device.device_id,"status": c.is_resolved,"desc":c.desc})
                else:
                    complaint_list.append({"pk": c.pk, "username": c.user.user.username, "type": c.type, "status": c.is_resolved,"desc":c.desc})
            complaint_list = sorted(complaint_list, key = lambda i: i['pk'],reverse=True)
            complaint_list = sorted(complaint_list, key = lambda i: i['status'],reverse=False)
            message = complaint_list
            code =200
        else:
            message = "You are a User, Not Authorised"
            code = 400
        content = {"message":message}
        return Response(data = content, status = code)


class ResolveComplaint(APIView):
    permission_classes = (IsAuthenticated, )

    def post(self, request):
        x = EndUser.objects.filter(user = request.user)[0]
        if x.is_admin:
            complaint = Complaint.objects.get(id = request.data['pk'])
            if not complaint.is_resolved:
                complaint.is_resolved = True
                complaint.save()
                message = "Complaint Resolved"
            else:
                message = "Complaint Already Resolved"
            code =200
        else:
            message = "You are a User, Not Authorised"
            code = 400
        content = {"message":message}
        return Response(data = content, status = code)
