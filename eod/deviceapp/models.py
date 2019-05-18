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
    avg_temp = models.IntegerField()
    avg_voc = models.IntegerField()
    avg_pres = models.IntegerField()
    smell_class = models.CharField(max_length = 100)

    def __str__(self):
        string = self.device.device_id + " -- " +self.smell_class
        return string
