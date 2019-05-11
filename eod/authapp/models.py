from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EndUser(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        if self.is_admin:
            string = self.user.username + " -- " + "Admin"
        else:
            string = self.user.username + " -- " + "User"
        return string
