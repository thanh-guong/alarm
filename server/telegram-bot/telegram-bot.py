#!/usr/bin/env python

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import Bot

SUBSCRIBERS_FILENAME = "subscribers"
SECRETS_FILENAME = "secrets"

import paho.mqtt.client as mqtt

MQTT_HOST = "mosquitto"
MQTT_PORT = 1883
MQTT_CONSUME_TOPIC = "alarm/home-to-garage-proxy"

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)


# SUPPORT FUNCTIONS


def create_file_if_doesnt_exist(filename):
    file = open(filename, "a")
    file.close()


def get_telegram_bot_subscribers():
    file = open(SUBSCRIBERS_FILENAME, "r")
    subscribers = file.readlines()
    file.close()
    return subscribers


def secret():
    file = open(SECRETS_FILENAME, "r")
    secret = file.readline()
    file.close()
    return secret


def forward_message_to_subscribers(message):
    # forward message to Telegram bot subscribers
    bot = Bot(secret())
    subscribers = get_telegram_bot_subscribers()
    for subscriber in subscribers:
        bot.sendMessage(chat_id=subscriber.strip("\n"), text=message)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def subscribe(update, context):
    exists = False

    user_id = str(update.message.chat.id)

    subscribers = get_telegram_bot_subscribers()

    for subscriber in subscribers:
        if user_id == subscriber.strip("\n"):
            exists = True

    if not exists:
        file = open(SUBSCRIBERS_FILENAME, "a")
        if file.write(user_id + "\n") < 1:
            update.message.reply_text("Something gone wrong")
        else:
            update.message.reply_text("You subscribed!")
        file.close()
    else:
        update.message.reply_text("You're already a subscriber")


def unsubscribe(update, context):
    user_id = str(update.message.chat.id)

    subscribers = get_telegram_bot_subscribers()

    # rewrite every subscriber
    file = open(SUBSCRIBERS_FILENAME, "w")
    for subscriber in subscribers:
        if user_id != subscriber.strip("\n"):
            file.write(str(subscriber) + "\n")

    file.close()
    update.message.reply_text("Subscription removed")


def telegram_bot():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(secret(), use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("subscribe", subscribe))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # Start the Bot
    updater.start_polling()


# The callback for when the client receives a CONNACK response from the server.
def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_CONSUME_TOPIC)

    message = "Telegram bot subscribed to this topic: " + MQTT_CONSUME_TOPIC
    forward_message_to_subscribers(message)


# The callback for when a PUBLISH message is received from the server.
def mqtt_on_message(client, userdata, msg):
    message = "TOPIC: [ " + msg.topic + " ] " + str(msg.payload)

    print(message)

    forward_message_to_subscribers(message)


def mqtt_consumer():
    client = mqtt.Client()
    client.on_connect = mqtt_on_connect
    client.on_message = mqtt_on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()


def main():
    telegram_bot()
    mqtt_consumer()


if __name__ == '__main__':
    create_file_if_doesnt_exist(SUBSCRIBERS_FILENAME)
    create_file_if_doesnt_exist(SECRETS_FILENAME)
    main()
