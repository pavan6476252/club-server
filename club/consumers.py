from channels.generic.websocket import AsyncWebsocketConsumer
import json

class BookingNotificationConsumer(AsyncWebsocketConsumer):
    print("step-2")
    async def connect(self):
        self.resto_owner_id = self.scope['url_route']['kwargs']['resto_owner_id']

        # Join the group specific to the resto_owner
        self.group_name = f'resto_{self.resto_owner_id}_owners'
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
        # Send the notification message to the connected WebSocket consumer
        await self.send(json.dumps(event))
