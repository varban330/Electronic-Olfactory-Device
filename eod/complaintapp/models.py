from django.db import models
from authapp.models import EndUser
from deviceapp.models import Device

# Create your models here.
class Complaint(models.Model):
    user = models.ForeignKey(EndUser, on_delete = models.CASCADE, related_name='user_id_complaint')
    type = models.CharField(max_length = 10)
    device = models.ForeignKey(Device, on_delete = models.CASCADE,related_name='device_id_complaint', null = True)
    desc = models.CharField(max_length = 1000)
    is_resolved = models.BooleanField(default = False)

    def __str__(self):
        string = str(self.pk) + self.user.user.username + "--" + self.type
        return string
