import base64
from PIL import Image
import io
import json
from datetime import datetime
from django.core.files.base import ContentFile

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.core.files.storage import default_storage

from api.models import APIProduct
from chat.models import Message, Tag
from chat.serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        self.user = self.scope["user"]

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def parse_and_add_tags(self, message):
        text = message.split(' ')
        text = list(filter(None, text))
        tags = [t for t in text if t[0] == '#']
        ls_tags = []
        for tag in tags:
            tag = tag.lower()
            tag_obj, created = await sync_to_async(Tag.objects.get_or_create, thread_sensitive=True)(tag_text=tag[1:])
            ls_tags.append(tag_obj)

        return ls_tags

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        upvote = '0'
        downvote = '0'
        topic = text_data_json.get('roomName')
        file = text_data_json.get('file')
        user = self.user

        try:
            ls_tags = []
            if message.rstrip() != '':
                ls_tags = await self.parse_and_add_tags(message)

            if file:
                format, imgstr = file.split(';base64,')
                ext = format.split('/')[-1]

                file_data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
                file_data.name = f"{topic}/{file_data.name}"
            else:
                file_data = None

            # save image under message_images
            # image = base64.b64decode(file)
            # file_name = 'test.jpeg'
            # attachment_name = default_storage.save('message_images/{0}'.format(file.name), file) if file else ''

            # image_path = (f'message_images/{file_name}/')
            # img = Image.open(io.BytesIO(image))
            # img.save(image_path, 'jpeg')

            api_product = await sync_to_async(APIProduct.objects.get, thread_sensitive=True)(name=topic)
            results = await sync_to_async(Message.objects.create, thread_sensitive=True)(user=user, description=message,
                                                                                         topic=api_product,
                                                                                         file=file_data)
            # if the message was not empty then add the list of parsed tags into the list
            if ls_tags:
                await sync_to_async(results.message_tags.add, thread_sensitive=True)(*ls_tags)
                await sync_to_async(results.save, thread_sensitive=True)()


            # Send message to WebSocket
        except APIProduct.DoesNotExist as e:
            # This chat-room does not exist
            pass

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'id': results.id,
                'message': message,
                'upvote': upvote,
                'downvote': downvote,
                'room_name': self.room_name,
                'file': results.file.name,
                'username': user.username,
                'city': user.city,
                'region': user.region,
                'country': user.country,
                'created_at': f"{datetime.now().strftime('%Y-%m-%d %H:%M')}",
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        id = event['id']
        message = event['message']
        upvote = event['upvote']
        downvote = event['downvote']
        username = event['username']
        city = event['city']
        region = event['region']
        country = event['country']
        created_at = event['created_at']
        file = event['file']
        # user = self.user.username

        # Send message to WebSocket
        # file name in the view does not have the /uploads prefixed to the start, since it uses the default MEDIA_ROOT
        await self.send(text_data=json.dumps({
            'id': id,
            'message': f"{message} - {username} - {created_at} -  {city}, {region}, {country}",
            'upvote': upvote,
            'downvote': downvote,
            'file': f"/uploads/{file}",
        }))
