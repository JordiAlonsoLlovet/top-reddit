from telegram.ext import Updater, CommandHandler
import os


def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

TOKEN = os.getenv("TOKEN")
updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()
