from django.db import models
from authapp.models import EndUser

# Create your models here.
class Device(models.Model):
    user = models.ForeignKey(EndUser, on_delete = models.CASCADE, related_name="user_id_device")
    device_id = models.CharField(max_length = 8, unique= True)

    def __str__(self):
        string = self.device_id + " -- " +self.user.user.username
        return string

class DeviceLog(models.Model):
    device = models.ForeignKey(Device, on_delete = models.CASCADE, related_name="device_id_log")
    avg_temp = models.FloatField()
    avg_co = models.FloatField(default = 0.0)
    avg_lpg = models.FloatField(default = 0.0)
    avg_smoke = models.FloatField(default = 0.0)
    avg_pres = models.FloatField()
    smell_class = models.CharField(max_length = 100)
    pushed = models.BooleanField(default = False)

    def __str__(self):
        string = self.device.device_id + " -- " +self.smell_class
        return string

class DangerLog(models.Model):
    device = models.ForeignKey(Device, on_delete = models.CASCADE, related_name="danger_id_log")
    avg_temp = models.FloatField()
    avg_co = models.FloatField(default = 0.0)
    avg_lpg = models.FloatField(default = 0.0)
    avg_smoke = models.FloatField(default = 0.0)
    avg_pres = models.FloatField()
    smell_class = models.CharField(max_length = 100)
    pushed = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now = True)

    def __str__(self):
        string = self.device.device_id + " -- " +self.smell_class
        return string
