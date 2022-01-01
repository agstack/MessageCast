from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import APIProduct, User


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'usage', 'address', 'city', 'state', )


class APIProductSerializer(ModelSerializer):
    subscribers = UsersSerializer(many=True)

    class Meta:
        model = APIProduct
        fields = ('name', 'about', 'logo', 'active', 'subscribers', )
