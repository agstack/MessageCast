from django.contrib.auth.models import AbstractUser
from django.db import models
import random


def generate_token():
    return str(random.randint(1000000000, 9999999999))


class User(AbstractUser):
    phone = models.CharField(max_length=255, verbose_name='phone')
    usage = models.CharField(max_length=255, verbose_name='usage', choices=(('c', 'commercial'),
                                                                            ('r', 'research'),
                                                                            ('e', 'educational'),
                                                                            ('g', 'government')))
    address = models.CharField(max_length=255, verbose_name='address', null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name='city', null=True, blank=True)
    state = models.CharField(max_length=255, verbose_name='state', null=True, blank=True)
    country = models.CharField(max_length=255, verbose_name='country', null=True, blank=True, default='USA')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return 'User: ' + str(self.username)


class APIProduct(models.Model):
    name = models.CharField(max_length=255, verbose_name='name')
    about = models.CharField(max_length=255, verbose_name='about')
    logo = models.FileField(null=True, blank=True)
    active = models.BooleanField(default=False)
    subscribers = models.ManyToManyField('User', blank=True, verbose_name='subscribers')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        active = 'Active' if self.active else 'Non-Active'
        return f'{active} - {self.name}'


class Subscription(models.Model):
    token = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        unique=True,
        default=generate_token
    )
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    api_product = models.ForeignKey('APIProduct', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        active = 'Active' if self.status else 'Non-Active'
        return f'{active} - {self.user.username} - {self.api_product.name}'
