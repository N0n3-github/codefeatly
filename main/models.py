from django.db import models
from django.contrib.auth.models import User as BaseUser


class User(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    rank = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Profile"
