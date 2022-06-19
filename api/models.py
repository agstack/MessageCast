import uuid

import h3
import ip2geotools
from django.contrib.auth.models import AbstractUser
from django.db import models
import random

import s2sphere as s2
from ip2geotools.databases.noncommercial import DbIpCity


def generate_token():
    return str(random.randint(1000000000, 9999999999))


class User(AbstractUser):
    phone = models.CharField(max_length=255, verbose_name='phone')
    usage = models.CharField(max_length=255, verbose_name='usage', choices=(('c', 'commercial'),
                                                                            ('r', 'research'),
                                                                            ('e', 'educational'),
                                                                            ('g', 'government')))
    ip = models.CharField(max_length=255, verbose_name='ip', null=True, blank=True)
    region = models.CharField(max_length=255, verbose_name='region', null=True, blank=True)
    city = models.CharField(max_length=255, verbose_name='city', null=True, blank=True)
    country = models.CharField(max_length=255, verbose_name='country', null=True, blank=True, default='USA')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.CharField(max_length=255, verbose_name='latitude', null=True, blank=True)
    longitude = models.CharField(max_length=255, verbose_name='longitude', null=True, blank=True)
    h3_index = models.CharField(max_length=255, verbose_name='h3_index', null=True, blank=True)
    h3_resolution = models.CharField(max_length=255, verbose_name='h3_resolution', default=12)
    s2_index = models.CharField(max_length=255, verbose_name='s2_index', null=True, blank=True)
    s2_level = models.CharField(max_length=255, verbose_name='s2_level', default=20)
    discoverable = models.BooleanField(default=False)

    def __str__(self):
        return 'User: ' + str(self.username)

    def save(self, *args, **kwargs):
        if self.discoverable:
            try:
                # H3 index implementation
                if self.ip:
                    response = DbIpCity.get(self.ip, api_key='free')

                    self.latitude = response.latitude
                    self.longitude = response.longitude
                    self.city = response.city
                    self.region = response.region
                    self.country = response.country

                    self.h3_index = h3.geo_to_h3(self.latitude, self.longitude, int(self.h3_resolution))
            except ip2geotools.errors.InvalidRequestError or ConnectionError or Exception as e:
                pass

            try:
                # S2 implementation
                cell = s2.Cell.from_lat_lng(s2.LatLng.from_degrees(self.latitude, self.longitude))
                cid = cell.id().parent(int(self.s2_level))
                self.s2_index = cid.to_token()
            except:
                pass
        super().save(*args, **kwargs)


class APIProduct(models.Model):
    name = models.CharField(max_length=255, verbose_name='name', unique=True)
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
    # this is the uuid
    token = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name='uuid')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    api_product = models.ForeignKey('APIProduct', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    name = models.CharField(max_length=255, verbose_name='name', default='', null=True, blank=True)
    latitude = models.CharField(max_length=255, verbose_name='latitude', default='', null=True, blank=True)
    longitude = models.CharField(max_length=255, verbose_name='longitude', default='', null=True, blank=True)

    def __str__(self):
        active = 'Active' if self.status else 'Non-Active'
        return f'{active} - {self.user.username} - {self.api_product.name}'
