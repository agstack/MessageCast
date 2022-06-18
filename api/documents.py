# from django_elasticsearch_dsl import (
#     Document,
#     fields,
#     Index,
# )
# from .models import APIProduct
#
# PUBLISHER_INDEX = Index('api_product')
#
# PUBLISHER_INDEX.settings(
#     number_of_shards=1,
#     number_of_replicas=1
# )
#
#
# @PUBLISHER_INDEX.doc_type
# class APIProductDocument(Document):
#     id = fields.IntegerField(attr='id')
#     fielddata = True
#     name = fields.TextField(
#         fields={
#             'raw': {
#                 'type': 'keyword',
#             }
#
#         }
#     )
#     about = fields.TextField(
#         fields={
#             'raw': {
#                 'type': 'keyword',
#
#             }
#         },
#     )
#
#     class Django(object):
#         model = APIProduct

from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
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
        model = APIProduct # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'name',
            'about',
        ]
