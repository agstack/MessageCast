from django.db.models.functions import TruncMonth
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
        fields = ('token', 'user', 'api_product', 'status', 'created_at', )


class SubscriptionMonthYearSerializer(ModelSerializer):
    month_year = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('month_year', )

    def get_month_year(self, obj):
        try:
            return f"{obj.created_at.month}/{obj.created_at.year}"
        except:
            return None


class SubscriptionCountrySerializer(ModelSerializer):
    country = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('country', )

    def get_country(self, obj):
        try:
            return obj.user.country
        except:
            return None


class SubscriptionUsageSerializer(ModelSerializer):
    usage = serializers.SerializerMethodField()

    class Meta:
        model = Subscription
        fields = ('usage', )

    def get_usage(self, obj):
        try:
            return obj.user.usage
        except:
            return None

