"""
This element is a consumer for the messages coming from alarm element, and a producer for the Telegram bot proxy.
"""

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

MQTT_HOST = "remote-mosquitto-host"
MQTT_PORT = 1883
MQTT_CONSUME_TOPIC = "alarm/to-garage-proxy"
MQTT_PRODUCE_TOPIC = "alarm/home-to-garage-proxy"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # TODO
    print("i'm alive")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # TODO
    print("i'm alive")


def main():
    # TODO
    print("i'm alive")


if __name__ == '__main__':
    main()
