import pytz
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Device, DeviceLog, DangerLog
from rest_framework.views import APIView
from rest_framework.response import Response
from authapp.models import EndUser
from .functions import log_generator, save_device_status
from datetime import datetime

tz = pytz.timezone('Asia/Kolkata')

api_key = '94cea4adae3c452ebd3c2ff10dd54d7c'

dangerous = ["Ethanol"]

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
            if request.META["HTTP_OCP_APIM_SUBSCRIPTION_KEY"] == api_key and save_device_status(request.data):
                content = {
                "message": "Logs Changed",
                }
                status = 200
            else:
                content = {
                "message": "Sorry You can't send request to this source",
                }
                status = 401
        except:
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
            # log_generator(device)
            device_status = DeviceLog.objects.filter(device = device)[0]
            content = {
            "device_id": device.device_id,
            "smell_class": device_status.smell_class,
            "avg_temp": device_status.avg_temp,
            "avg_pres": device_status.avg_pres,
            "avg_co": device_status.avg_co,
            "avg_lpg": device_status.avg_lpg,
            "avg_smoke": device_status.avg_smoke,
            }
            status = 200
        except:
            content = {
            "message": "Error Occurred Send Correct Data",
            }
            status = 400
        return Response(data = content, status = status)


class PushNotifications(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            x = EndUser.objects.filter(user = request.user)[0]
            devices = Device.objects.filter(user = x)
            notification_list = []
            for device in devices:
                device_statuses = DangerLog.objects.filter(device = device)
                print(device)
                print(device_statuses)
                for device_status in device_statuses:
                    if device_status.pushed == False and device_status.smell_class in dangerous:
                        content = {
                            "device_id": device.device_id,
                            "smell_class": device_status.smell_class,
                            "avg_temp": device_status.avg_temp,
                            "avg_pres": device_status.avg_pres,
                            "avg_co": device_status.avg_co,
                            "avg_lpg": device_status.avg_lpg,
                            "avg_smoke": device_status.avg_smoke,
                            "timestamp": device_status.timestamp.astimezone(tz).strftime("%d/%m/%Y, %H:%M:%S")
                        }
                        device_status.pushed = True
                        device_status.save()
                        notification_list.append(content)
                print(notification_list)

                content = {
                    "notifications": notification_list
                }
                status = 200
        except:
            content = {
            "message": "An Error Occurred",
            }
            status = 400
        return Response(data = content, status = status)


class PushNotificationHistory(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        try:
            x = EndUser.objects.filter(user = request.user)[0]
            devices = Device.objects.filter(user = x)
            notification_list = []
            for device in devices:
                device_statuses = DangerLog.objects.filter(device = device)
                for device_status in device_statuses:
                    content = {
                        "device_id": device.device_id,
                        "smell_class": device_status.smell_class,
                        "avg_temp": device_status.avg_temp,
                        "avg_pres": device_status.avg_pres,
                        "avg_co": device_status.avg_co,
                        "avg_lpg": device_status.avg_lpg,
                        "avg_smoke": device_status.avg_smoke,
                        "timestamp": device_status.timestamp.astimezone(tz).strftime("%d/%m/%Y, %H:%M:%S")
                    }
                    notification_list.append(content)
                print(notification_list)

                notification_list = sorted(notification_list, key = lambda i: datetime.strptime(i['timestamp'], "%d/%m/%Y, %H:%M:%S"),reverse=True)
                content = {
                    "notifications": notification_list
                }
                status = 200
        except:
            content = {
            "message": "An Error Occurred",
            }
            status = 400
        return Response(data = content, status = status)
