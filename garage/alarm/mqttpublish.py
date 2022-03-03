import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
MQTT_PORT = 1883
MQTT_PRODUCE_TOPIC = "alarm/status"


def publish_alarm_status(status):
    publish.single(MQTT_PRODUCE_TOPIC, status, hostname=MQTT_HOST, port=MQTT_PORT)
