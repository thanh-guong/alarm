"""
This element is a consumer for the messages coming from garage, and a producer for the Telegram bot.
"""

import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt

MQTT_HOST = "mosquitto"
MQTT_PORT = 1883
MQTT_CONSUME_TOPIC = "alarm/alarm"
MQTT_PRODUCE_TOPIC = "alarm/alarm"


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_CONSUME_TOPIC)

    message = "Connected to message broker"

    publish.single(MQTT_PRODUCE_TOPIC, message, hostname=MQTT_HOST)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    message = "TOPIC: [ " + msg.topic + " ] " + str(msg.payload)

    print(message)

    # just forward the received message to the telegram-bot application
    publish.single(MQTT_PRODUCE_TOPIC, message, hostname=MQTT_HOST)


def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()


if __name__ == '__main__':
    main()
