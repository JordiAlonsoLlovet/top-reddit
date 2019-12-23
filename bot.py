import logging
import praw
import sys
import os

from telegram.ext import Updater, CommandHandler

# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

#Creating a read-only Reddit instance
reddit = praw.Reddit(client_id='DhuZOjJy8UoelQ',
                     client_secret='xX_cP0bUNdxiBwxXlStUNAuZUh8',
                     user_agent='windows:telegramBot:v.1.0.0 (by /u/top-reddit-bot)')

# Getting mode, so we could define run function for local and Heroku setup
mode = sys.argv[1]
TOKEN = sys.argv[2]
if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def start_handler(bot, update):
    # Creating a handler-function for /start command 
    logger.info("User {} started bot".format(update.effective_user["id"]))
    update.message.reply_text("Welcome to TopRedditBot! This bot allows you to find today's top post for your favourite subreddits\nPress Type /reddit <subreddit> to get a Top Post")


def reddit_handler(bot, update):
    request= update.message.text.split(" ", 1)
    subreddit = request[-1].split("/")
    logger.info("Searching for {} subreddit".format(subreddit))
    try:
        for submission in reddit.subreddit(subreddit[-1]).top('day',limit=1):
            update.message.reply_text(submission.url)
    except:
        update.message.reply_text("Oops, this subreddit doesn't exist or has restricted acces. Please try another one")


if __name__ == '__main__':
    logger.info("Starting bot")
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler("start", start_handler))
    updater.dispatcher.add_handler(CommandHandler("reddit", reddit_handler))

    run(updater)
