import time
from rest_framework import serializers

from chat.models import Message, Tag
from django_elasticsearch_dsl_drf.serializers import DocumentSerializer
from api.documents import MessageDocument


class MessageSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    city = serializers.CharField(source='user.city')
    country = serializers.CharField(source='user.country')
    region = serializers.CharField(source='user.region')
    created_at = serializers.SerializerMethodField('get_created_at')

    def get_created_at(self, obj): return obj.created_at.strftime('%Y-%m-%d %H:%M')

    class Meta:
        model = Message
        fields = ('id', 'description', 'username', 'created_at', 'city', 'country', 'region', 'upvote', 'downvote',
                  'file', )


class TagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(source='tag_text')

    class Meta:
        model = Tag
        fields = ('tag', )


class MessageDocumentSerializer(DocumentSerializer):

    class Meta(object):
        """Meta options."""
        model = Message
        document = MessageDocument
        fields = ('id', 'description', 'topic')

        def get_location(self, obj):
            """Represent location value."""
            try:
                return obj.location.to_dict()
            except:
                return {}
