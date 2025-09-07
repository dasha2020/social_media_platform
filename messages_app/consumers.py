import json
from channels.generic.websocket import AsyncWebsocketConsumer


from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.username = self.scope['url_route']['kwargs']['username']
        self.user = self.scope['user']
        self.other_user = await self.get_user(self.username)

        if self.other_user == self.user:
            await self.close()  
            return

        users = sorted([self.user.username, self.other_user.username])
        self.room_name = f'chat_{users[0]}_{users[1]}'
        self.room_group_name = f'chat_{self.room_name}'

        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message'].strip()
        if not message:
            return

        chat = await self.get_or_create_chat(self.user, self.other_user)


        await self.save_message(chat, self.user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': self.user.username,
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
        }))

    @database_sync_to_async
    def get_user(self, username):
        from django.contrib.auth.models import User
        return User.objects.get(username=username)

    @database_sync_to_async
    def get_or_create_chat(self, user1, user2):
        from .models import Chat, ChatMessage
        if user1.id < user2.id:
            return Chat.objects.get_or_create(user1=user1, user2=user2)[0]
        else:
            return Chat.objects.get_or_create(user1=user2, user2=user1)[0]

    @database_sync_to_async
    def save_message(self, chat, sender, text):
        from .models import Chat, ChatMessage
        return ChatMessage.objects.create(chat=chat, user=sender, text=text)
