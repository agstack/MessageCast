from django.db import models
from django.db.models import ManyToManyField

from api.models import User, APIProduct


class Tag(models.Model):
    tag_text = models.CharField(max_length=2000, verbose_name='tag_text')


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(APIProduct, on_delete=models.CASCADE, verbose_name='topic')
    description = models.CharField(max_length=2000, verbose_name='description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, null=True)
    message_tags = models.ManyToManyField(Tag)
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)
    upvoters = ManyToManyField(User, null=True, blank=True, related_name='upvoters')
    downvoters = ManyToManyField(User, null=True, blank=True, related_name='downvoters')


