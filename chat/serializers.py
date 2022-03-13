import time
from rest_framework import serializers

from chat.models import Chat


class ChatSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    city = serializers.CharField(source='user.city')
    country = serializers.CharField(source='user.country')
    region = serializers.CharField(source='user.region')
    created_at = serializers.SerializerMethodField('get_created_at')

    def get_created_at(self, obj): return obj.created_at.strftime('%Y-%m-%d %H:%M')

    class Meta:
        model = Chat
        fields = ('message', 'username', 'created_at', 'city', 'country', 'region')
