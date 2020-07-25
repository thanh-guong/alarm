#!/usr/bin/env python

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import Bot

import paho.mqtt.client as mqtt

SUBSCRIBERS_FILENAME = "subscribers"
SECRETS_FILENAME = "secrets"

MQTT_HOST = "mqtt"
MQTT_PORT = 1883
MQTT_TOPIC = "thanh-guong-alarm"


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


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


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


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_TOPIC)

    bot = Bot(secret())
    subscribers = get_telegram_bot_subscribers()

    message = "Connected to message broker"

    for sub in subscribers:
        bot.send_message(sub, message)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    bot = Bot(secret())
    subscribers = get_telegram_bot_subscribers()

    message = msg.topic + " " + str(msg.payload)

    for sub in subscribers:
        bot.send_message(sub.strip("\n"), message)
    print(msg.topic + " " + str(msg.payload))


def main():

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

    # MQTT

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(MQTT_HOST, MQTT_PORT, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    # create file if doesn't exist
    file = open(SUBSCRIBERS_FILENAME, "a")
    file.close()

    # create file if doesn't exist
    file = open(SECRETS_FILENAME, "a")
    file.close()

    main()
