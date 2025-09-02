from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
# from .models import SensorData

import time

@shared_task
def handle_device_event(payload: dict):
    """
    Called whenever an MQTT message is received from ESP32.
    """

    """
    payload example:
    {
      "loudness_value": 32.2,
      "is_sitting": true
    }
    """
    from sensor.models import SensorData
    SensorData.objects.create(**payload)

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "sensor_data",
        {"type": "sensor.update", "message": payload},

    )