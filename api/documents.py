from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry

from chat.models import Message
from .models import APIProduct


@registry.register_document
class APIProductDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'api_product'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        # The model associated with this Document
        model = APIProduct

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['name', 'about', 'logo', 'active']


@registry.register_document
class MessageDocument(Document):
    class Index:
        # Name of the Elasticsearch index
        name = 'chat_message'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        # The model associated with this Document
        model = Message

        # The fields of the model you want to be indexed in Elasticsearch
        fields = ['description']
