from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import os
from captcha import generate_math_captcha
from utils.helpers import *


def make_sure_telegram(update: Update, context):
    update.message.reply_text(
        "Please join our telegram group to continue")
    return JOIN_TELEGRAM


def make_sure_twitter(update: Update, context):
    update.message.reply_text("Please follow us on twitter to continue")
    return JOIN_TWITTER


def make_sure_linkedin(update: Update, context):
    update.message.reply_text("Please connect with us on linkedin to continue")
    return JOIN_LINKEDIN


def make_sure_instagram(update: Update, context):
    update.message.reply_text("Please follow us on instagram to continue")
    return JOIN_INSTAGRAM


def make_sure_facebook(update: Update, context):
    update.message.reply_text("Please like our facebook page to continue")
    return JOIN_FACEBOOK


def start_command(update: Update, context):
    captcha_results = generate_math_captcha()
    update.message.reply_photo(photo=open(
        'captcha_maze/math.png', 'rb'), caption='Please answer the following math to prove you are a human 👇👇👇')
    update.message.reply_text(text=f'The correct answer is: {
                              captcha_results}', reply_markup=create_reply_markup())
    return ConversationHandler.END


def main():
    print('Bot started')
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', start_command)],
        states={
            JOIN_TELEGRAM: [MessageHandler(Filters.text, make_sure_telegram)],
            JOIN_TWITTER: [MessageHandler(Filters.text, make_sure_twitter)],
            JOIN_LINKEDIN: [MessageHandler(Filters.text, make_sure_linkedin)],
            JOIN_INSTAGRAM: [MessageHandler(Filters.text, make_sure_instagram)],
            JOIN_FACEBOOK: [MessageHandler(Filters.text, make_sure_facebook)]
        },
        fallbacks=[CommandHandler('start', start_command)]
    ))

    dispatcher.add_handler(CommandHandler('start', start_command))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
