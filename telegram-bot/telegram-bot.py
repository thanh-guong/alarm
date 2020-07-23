#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

SUBSCRIBERS_FILENAME = "subscribers"
SECRETS_FILENAME = "secrets"

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help_command(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def subscribe(update, context):
    exists = False

    user_id = str(update.message.chat.id)

    file = open(SUBSCRIBERS_FILENAME, "r")
    lines = file.readlines()
    file.close()

    for line in lines:
        if user_id == line.strip("\n"):
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

    file = open(SUBSCRIBERS_FILENAME, "r")
    lines = file.readlines()
    file.close()

    # rewrite every subscriber
    file = open(SUBSCRIBERS_FILENAME, "w")
    for line in lines:
        if user_id != line.strip("\n"):
            file.write(str(line))

    file.close()
    update.message.reply_text("Subscription removed")


def secret():
    file = open(SECRETS_FILENAME, "r")
    return file.readline()


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

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

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
