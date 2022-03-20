from django.db import models

from api.models import User, APIProduct


class Tag(models.Model):
    tag_text = models.CharField(max_length=2000, verbose_name='tag_text')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChatTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, verbose_name='tag')
    upvote = models.IntegerField(default=0)
    downvote = models.IntegerField(default=0)


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(APIProduct, on_delete=models.CASCADE, verbose_name='topic')
    description = models.CharField(max_length=2000, verbose_name='description')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, null=True)
    chat_tags = models.ManyToManyField(ChatTag)


