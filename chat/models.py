from django.db import models

from api.models import User, APIProduct


class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat_room = models.ForeignKey(APIProduct, on_delete=models.CASCADE, verbose_name='chat_api_product')
    message = models.CharField(max_length=2000, verbose_name='message')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to ='uploads/', height_field=None, width_field=None, null=True)
