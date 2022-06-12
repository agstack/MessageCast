import os
import uuid
from django.db import models
from django.db.models import ManyToManyField

from api.models import User, APIProduct


class Tag(models.Model):
    tag_text = models.CharField(max_length=2000, verbose_name='tag_text')


def get_file_path(instance, filename):
    directory = filename.split('/')[0]
    file_name = filename.split('/')[1]
    ext = file_name.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    # saving the image in a directory under the topic
    return os.path.join('message_images', f"{directory}/{filename}")


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
    file = models.FileField(upload_to=get_file_path, default=None, null=True)

