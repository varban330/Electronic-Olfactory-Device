from django.contrib import admin
from .models import Device, DeviceLog, DangerLog

# Register your models here.
admin.site.register(Device)
admin.site.register(DeviceLog)
admin.site.register(DangerLog)
