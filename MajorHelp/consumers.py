import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Load previous messages
        messages = await self.get_last_messages(self.room_name)
        for msg in messages:
            await self.send(text_data=json.dumps({
                'message': msg.content,
                'username': msg.user.username,
                'timestamp': msg.timestamp.strftime("%I:%M %p")
            }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = self.scope["user"].username if self.scope["user"].is_authenticated else "Guest"

        if self.scope["user"].is_authenticated:
            await self.save_message(data["message"], self.scope["user"], self.room_name)

        await self.channel_layer.group_send(self.room_group_name, {
            'type': 'chat_message',
            'message': data['message'],
            'username': username
        })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username']
        }))

    @database_sync_to_async
    def save_message(self, content, user, room):
        from .models import ChatMessage  # <–– move import inside the method
        return ChatMessage.objects.create(user=user, content=content, channel=room, timestamp=timezone.now())

    @database_sync_to_async
    def get_last_messages(self, room):
        from .models import ChatMessage  # <–– move import inside the method
        return ChatMessage.objects.filter(channel=room).order_by('-timestamp')[:25][::-1]
