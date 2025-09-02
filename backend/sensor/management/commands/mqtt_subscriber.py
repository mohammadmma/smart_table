# sensor/management/commands/mqtt_subscriber.py
import json
import os
import paho.mqtt.client as mqtt
from django.core.management.base import BaseCommand
from sensor.tasks import handle_device_event

BROKER_HOST = os.getenv("MQTT_BROKER", "mqtt")
BROKER_PORT = int(os.getenv("MQTT_PORT", "1883"))
TOPIC = os.getenv("MQTT_TOPIC", "sensors/data")

class Command(BaseCommand):
    help = "Run MQTT subscriber and forward messages to Celery"

    def handle(self, *args, **options):
        client = mqtt.Client(client_id="django_mqtt_subscriber", protocol=mqtt.MQTTv311)

        def on_connect(client, userdata, flags, rc):
            self.stdout.write(self.style.SUCCESS(f"Connected to MQTT (rc={rc})"))
            client.subscribe(TOPIC)
            self.stdout.write(self.style.SUCCESS(f"Subscribed to topic: {TOPIC}"))

        def on_message(client, userdata, msg):
            try:
                payload = json.loads(msg.payload.decode())
            except json.JSONDecodeError:
                self.stdout.write(self.style.WARNING(f"Invalid JSON: {msg.payload!r}"))
                return

            # Kick work to Celery (non-blocking)
            handle_device_event.delay(payload)

        client.on_connect = on_connect
        client.on_message = on_message
        client.connect(BROKER_HOST, BROKER_PORT, 60)
        client.loop_forever()
