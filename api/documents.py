from django_elasticsearch_dsl import Document, fields
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
    topic = fields.ObjectField(properties={
        'name': fields.TextField(),
        'about': fields.TextField(),
        'logo': fields.FileField(),
        'active': fields.TextField(),
    })

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
        fields = ['description', ]
        related_models = [APIProduct]

    def get_queryset(self):
        """Not mandatory but to improve performance we can select related in one sql request"""
        return super(MessageDocument, self).get_queryset().select_related(
            'topic'
        )

    # def get_instances_from_related(self, related_instance):
    #     """If related_models is set, define how to retrieve the Car instance(s) from the related model.
    #     The related_models option should be used with caution because it can lead in the index
    #     to the updating of a lot of items.
    #     """
    #     if isinstance(related_instance, APIProduct):
    #         return related_instance.car_set.all()
