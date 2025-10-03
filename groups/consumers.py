import base64
import imghdr
import uuid
from django.core.files.base import ContentFile


from channels.generic.websocket import AsyncWebsocketConsumer


from channels.db import database_sync_to_async

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.group_name = f"groupchat_{self.group_id}"
        self.user = self.scope['user']

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        import json
        from .models import Group, GroupMessage

        data = json.loads(text_data)
        message_text = data.get("message", "")
        image_data = data.get("image")
        sender = self.scope["user"]

        group = await database_sync_to_async(Group.objects.get)(id=self.group_id)


        if image_data:
            saved_message = await self.save_base64_image_with_text(group, sender, message_text, image_data)
        else:
            saved_message = await self.save_message(group, sender, message_text)

        if not saved_message:
            print("Message saving failed.")
            return

        
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat_message",
                "message": message_text,
                "sender": sender.username,
                "avatar_url": await self.get_avatar_url(sender),
                "image_url": saved_message.image.url if saved_message.image else None,
                #"is_me": sender.username == self.user.username
                "message_id": saved_message.id,
            }
        )

    async def chat_message(self, event):
        import json
        await self.send(text_data=json.dumps(event))

    

    @database_sync_to_async
    def save_message(self, group, sender, text):
        from .models import Group, GroupMessage
        return GroupMessage.objects.create(group=group, user=sender, text=text)
    
    @database_sync_to_async
    def save_base64_image_with_text(self, group, sender, text, base64_data):
        from .models import GroupMessage
        try:
            format, imgstr = base64_data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = base64.b64decode(imgstr)
            filename = f"{uuid.uuid4().hex}.{ext}"

            image_file = ContentFile(img_data, name=filename)

            return GroupMessage.objects.create(
                group=group,
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