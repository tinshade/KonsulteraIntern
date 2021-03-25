from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    choices = (('User', 'User'),('Admin', 'Administrator'))
    usertype = models.CharField('UserType',max_length=5, choices=choices, default='User')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)