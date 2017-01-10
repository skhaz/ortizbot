# -*- coding: utf-8 -*-
import os
import logging
import random
from google.appengine.ext import deferred
from google.appengine.ext import ndb
from google.appengine.api import app_identity

from flask import Blueprint, request

from telegram import Bot, Update
from telegram.ext import (
    Dispatcher,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    Filters
)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

blueprint = Blueprint('bot', __name__)

token = os.environ['TELEGRAM_TOKEN']
bot = Bot(token)
dispatcher = None


def reply(bot, update):
    quotes = [
        "Hahahaha",
    ]

    update.message.reply_text(random.choice(quotes))


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


@blueprint.before_app_first_request
def setup_webhook():
    global dispatcher

    dispatcher = Dispatcher(bot=bot, update_queue=None, workers=0)
    dispatcher.add_handler(MessageHandler(Filters.text, reply))
    dispatcher.add_error_handler(error)

    hostname = app_identity.get_default_version_hostname()
    bot.setWebhook(webhook_url='%s/telegram/%s' % (hostname, token))


@blueprint.route('/telegram/' + token, methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)

    return ('', 204)
