from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Device, DeviceLog
from rest_framework.views import APIView
from rest_framework.response import Response
from authapp.models import EndUser
from .functions import log_generator

api_key = '94cea4adae3c452ebd3c2ff10dd54d7c'
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


class SendDeviceStatus(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        try:
            if request.META["HTTP_OCP_APIM_SUBSCRIPTION_KEY"] == api_key:
                device = Device.objects.filter(device_id = request.data["device_id"])[0]
                filter_list = DeviceLog.objects.filter(device = device)
                if filter_list:
                    device_status = filter_list[0]
                else:
                    device_status = DeviceLog()
                    device_status.device = device
                device_status.smell_class = request.data["smell_class"]
                device_status.avg_temp = request.data["avg_temp"]
                device_status.avg_pres = request.data["avg_pres"]
                device_status.avg_voc = request.data["avg_voc"]
                device_status.save()
                content = {
                "message": "Logs Changed",
                }
                status = 200
            else:
                content = {
                "message": "Sorry You can't send request to this source",
                }
                status = 401
        except Exception as e:
            content = {
            "message": "Error Occurred Send Correct Data",
            }
            status = 400
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
