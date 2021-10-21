import logging

from telegram import Bot, Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, ConversationHandler
import random

import os
api_token = os.environ.get('API_TOKEN', None)

bot = Bot(api_token)

TYPING_USERS = range(1)

def send_message(update: Update, text: str):
    bot.send_message(chat_id=update.effective_chat.id, text=text)

def start(update: Update, context: CallbackContext) -> None:
    send_message(update, "Hello there! Here's the list of available commands:")
    help_command(update, CallbackContext)

def help_command(update: Update, context: CallbackContext) -> None:
    send_message(update, "/add - Add a list of users to select from\n/pick - Pick a random user")

def add_users_command(update: Update, context: CallbackContext) -> int:
    send_message(update, 'Please enter usernames (each on the new line):')
    return TYPING_USERS

def add_users(update: Update, context: CallbackContext) -> int:
    context.user_data['users'] = update.message.text.split('\n')
    send_message(update, 'Done! Now you can pick a random user with /pick!')
    return ConversationHandler.END

def pick_command(update: Update, context: CallbackContext) -> None:
    if 'users' in context.user_data:
        users = context.user_data['users']
        user = users[random.randint(0, len(users)-1)]
        send_message(update, f'{user} is the chosen one!')
    else:
        update.message.reply_text("You need to add users with the /add command first!")


def main() -> None:
    """Start the bot."""
    updater = Updater(api_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("pick", pick_command))
    dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('add', add_users_command)],
        states={
            TYPING_USERS: [
                MessageHandler(Filters.text & ~Filters.command, add_users)
            ],
        },
        fallbacks=[],
    ))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()