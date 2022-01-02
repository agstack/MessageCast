from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api.models import APIProduct, User, Subscription


class UsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'phone', 'email', 'usage', 'address', 'city', 'state', )


class APIProductSerializer(ModelSerializer):
    subscribers = UsersSerializer(many=True)

    class Meta:
        model = APIProduct
        fields = ('id', 'name', 'about', 'logo', 'active', 'subscribers', )


class SubscriptionSerializer(ModelSerializer):

    class Meta:
        model = Subscription
        fields = ('token', 'user', 'api_product', 'status', )

