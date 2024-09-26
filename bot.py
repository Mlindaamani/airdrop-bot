from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler,  MessageHandler, ContextTypes, Dispatcher, Filters, CallbackQueryHandler
from messages import RULES
from dotenv import load_dotenv
import os
from utils.helpers import create_inline_markup
from captcha import generate_math_captcha


# Load environment variables
load_dotenv('.env')


def start_command(update: Update, context: ContextTypes):
    results = generate_math_captcha()
    update.effective_message.reply_photo(photo=open(
        'captcha_maze/math.png', 'rb'), caption='Please answer the following math to prove you are a human 👇👇👇')
    update.message.reply_text(text=f'The correct answer is: {results}')


def inline_query_handlers(update: Update, context: ContextTypes):
    query = update.callback_query

    if query.data == 'telegram':
        update.callback_query.answer()
        update.callback_query.message.reply_text(
            text='PLEASE PROVIDE YOUR LOCATION AND PHONE NUMBER',
            reply_markup=ReplyKeyboardMarkup([
                [KeyboardButton(text='SEND LOCATION', request_location=True),
                 KeyboardButton(text='SEND CONTACT', request_contact=True)],
            ], resize_keyboard=True, one_time_keyboard=True))


def help_command(update: Update, context: ContextTypes):
    update.message.reply_text(
        "Please contact admin for help...")


def rules_command(update: Update, context: ContextTypes):
    update.message.reply_text(text=RULES)


def message_hander(update: Update, context: ContextTypes):
    message = update.effective_message.text.lower()

    if message == 'hello':
        username = update.effective_user.username
        context.user_data['username'] = username
        update.message.reply_text(f"Hello {username} How are you doing today?")
    elif message in ['great', 'fresh']:
        update.message.reply_text("Alright how can i be of the help")
    elif message == 'help':
        update.message.reply_text('Plaese click here /help for help')

    elif message == 'joke':
        update.message.reply_text('Do you want some jokes? YES OR NO')

    elif message == 'yes':
        update.message.reply_text('Do you know you can\'t really see me?😂😂')

    elif message == 'no':
        update.message.reply_text(
            'Oooh No maybe you want some music... right?')
    else:
        update.message.reply_text("I really don\'t understand your query")


def register_commands_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(CommandHandler('help', help_command))
    dispatcher.add_handler(CommandHandler('start', start_command))
    dispatcher.add_handler(CommandHandler('rules', rules_command))


def register_message_handlers(dispatcher: Dispatcher):
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, message_hander))


def register_inline_query_handler(dispatcher: Dispatcher):
    dispatcher.add_handler(CallbackQueryHandler(inline_query_handlers))


def main():
    updater = Updater(token=os.getenv('TOKEN'), use_context=True)
    dispatcher = updater.dispatcher

    print('Bot started...')
    register_inline_query_handler(dispatcher=dispatcher)
    register_commands_handlers(dispatcher=dispatcher)
    register_message_handlers(dispatcher=dispatcher)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
