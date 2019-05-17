from django.contrib import admin
from .models import Device, DeviceLog

# Register your models here.
admin.site.register(Device)
admin.site.register(DeviceLog)
