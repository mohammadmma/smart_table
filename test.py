import json, paho.mqtt.client as mqtt
c = mqtt.Client()
c.connect("localhost", 1883, 60)
c.publish("sensors/data", json.dumps({"loudness_value": 32.2, "is_sitting": True}))
c.disconnect()
