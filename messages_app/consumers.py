
import base64
import imghdr
import uuid
from django.core.files.base import ContentFile
from channels.db import database_sync_to_async

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
        import json
        from .models import Chat, ChatMessage
        from django.contrib.auth.models import User
        data = json.loads(text_data)

        sender = self.scope["user"]
        receiver_username = self.scope["url_route"]["kwargs"]["username"]
        receiver = await database_sync_to_async(User.objects.get)(username=receiver_username)

        message_text = data.get("message", "")
        image_data = data.get("image", None)

        chat = await self.get_or_create_chat(sender, receiver)
        saved_message = None

        if image_data:
            saved_message = await self.save_base64_image_with_text(chat, sender, message_text, image_data)
        else:
            saved_message = await self.save_message(chat, sender, message_text)

        if not saved_message:
            print("Message saving failed.")
            return

        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "sender": sender.username,
                "avatar_url": await self.get_avatar_url(sender),
                "image_url": saved_message.image.url if saved_message.image else None,
                "message_id": saved_message.id,
                
            }
        )

    async def chat_message(self, event):
        import json
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'sender': event['sender'],
            "avatar_url": event.get("avatar_url"),
            "image_url": event.get("image_url")
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
    
    @database_sync_to_async
    def save_base64_image_with_text(self, chat, sender, text, base64_data):
        from .models import ChatMessage
        try:
            format, imgstr = base64_data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = base64.b64decode(imgstr)
            filename = f"{uuid.uuid4().hex}.{ext}"

            image_file = ContentFile(img_data, name=filename)

            return ChatMessage.objects.create(
                chat=chat,
                user=sender,
                text=text,
                image=image_file
            )
        except Exception as e:
            print("Image save error:", e)
            return None
    
    @database_sync_to_async
    def get_avatar_url(self, user):
        if hasattr(user, "profile") and user.profile.avatar:
            return user.profile.avatar.url
        return None
