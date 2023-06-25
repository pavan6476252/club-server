from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json

class BookingNotificationConsumer(AsyncWebsocketConsumer):
    print("step-3")
    async def connect(self):
        self.resto_owner_id = self.scope['url_route']['kwargs']['resto_owner_id']

        # Join the group specific to the resto_owner
        self.group_name = f'resto_{self.resto_owner_id}_owners'
        print(self.group_name)
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group when the WebSocket connection is closed
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )
        
    

    async def notification_message(self, event):
        
        print("Received notification message:", event)
        await self.send(json.dumps(event))

