import datetime
import json,logging
from channels.generic.websocket import AsyncWebsocketConsumer  
from asgiref.sync import sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'chat_anon' 
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        logging.info(f'[{self.channel_name}] - You are connected to the chat room')

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        logging.info(f'[{self.channel_name}] - You are disconnected to the chat room')

    async def receive(self, text_data):
        from .models import Message,User
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        username = text_data_json.get('username')
        image = text_data_json.get('image')
        user = await User.objects.aget(username=username)
        if message:
            await Message.objects.acreate(text=message, user= user)
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )
        elif image:
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'image': image,
                'username': username
            }
        )

    async def chat_message(self, event):
        message = event.get('message')
        username = event.get('username')
        image = event.get('image')
        data = {'username': username}
        if message:
            data['message'] = message
        if image:
            data['image'] = image

        await self.send(text_data=json.dumps(data))