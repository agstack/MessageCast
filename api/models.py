from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone = models.CharField(max_length=255, verbose_name='phone')
    usage = models.CharField(max_length=255, verbose_name='usage')
    address = models.CharField(max_length=255, verbose_name='address')
    city = models.CharField(max_length=255, verbose_name='city')
    state = models.CharField(max_length=255, verbose_name='state')
    country = models.CharField(max_length=255, verbose_name='country')

    def __str__(self):
        return 'User: ' + str(self.username)


class APIProduct(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    about = models.CharField(max_length=255, verbose_name='about')
    logo = models.FileField(null=True, blank=True)
    active = models.BooleanField(default=False)
    subscribers = models.ManyToManyField('User', blank=True, verbose_name='subscribers')

    def __str__(self):
        active = 'Active' if self.approve else 'Non-Active'
        return f'{active} - {self.name}'
