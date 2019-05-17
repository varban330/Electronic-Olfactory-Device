from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from .models import Device, DeviceLog
from rest_framework.views import APIView
from rest_framework.response import Response
from authapp.models import EndUser
from .functions import log_generator

# Create your views here.
class RegisterDevice(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            x = EndUser.objects.filter(user = request.user)[0]
            if x.is_admin:
                dev = Device()
                dev.user=x
                dev.device_id = request.data["device_id"]
                dev.save()
                content = {
                "message": "Registration of Device Successful",
                "user": x.user.username,
                "device_id": dev.device_id
                }
                status = 200
            else:
                content = {
                "message": "Registration Failed"
                }
                status = 400
        except:
            content = {
            "message": "Registration Failed"
            }
            status = 400
        return Response(data = content, status = status)


class RegisterOwnDevice(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        x = EndUser.objects.filter(user = request.user)[0]
        if x.is_admin:
            content = {
            "message": "Registration Failed"
            }
            status = 400
        else:
            dev = Device.objects.filter(device_id = request.data["device_id"])
            if not dev:
                content = {
                "message": "No such Device"
                }
                status = 400
            else:
                y = dev[0].user
                if y.is_admin:
                    dev[0].user = x
                    dev[0].save()
                    content = {
                    "message": "Registration of Device Successful",
                    "user": request.user.username,
                    "device_id": dev[0].device_id
                    }
                    status = 200
                else:
                    content = {
                    "message": "Device already registered to other user",
                    }
                    status = 400

        return Response(data = content, status = status)


class GetDeviceList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        x = EndUser.objects.filter(user = request.user)[0]
        devices = Device.objects.filter(user = x)
        devices_list =  [dev.device_id for dev in devices]
        content = {
        "devices_list": devices_list
        }
        status = 200
        return Response(data = content, status = status)


class DeviceStatus(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self,request):
        try:
            device = Device.objects.filter(device_id = request.data["device_id"])[0]
            log_generator(device)
            device_status = DeviceLog.objects.filter(device = device)[0]
            content = {
            "device_id": device.device_id,
            "smell_class": device_status.smell_class,
            "avg_temp": device_status.avg_temp,
            "avg_pres": device_status.avg_pres,
            "avg_voc": device_status.avg_voc,
            }
            status = 200
        except:
            content = {
            "message": "Error Occurred Send Correct Data",
            }
            status = 400
        return Response(data = content, status = status)
