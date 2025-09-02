import json
from channels.generic.websocket import AsyncWebsocketConsumer

class SensorConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # group per-project; you can switch to per-user/device: f"user_{user_id}"
        self.group_name = "sensor_data"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    # Celery will send events with type="sensor.update"
    async def sensor_update(self, event):
        await self.send(text_data=json.dumps(event["message"]))