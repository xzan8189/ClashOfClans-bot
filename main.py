import os

from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update
from webserver import keep_alive
from settings.telegram import Telegram
from settings.clash_of_clans import Clash_of_clans

BOT_TOKEN = os.environ['Bot_token']
COC_TOKEN = os.environ['Clash_of_clans_API_token']

# Instance variables
updater = Updater(BOT_TOKEN, use_context=True)


def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    print("L'utente " + str(user) + " ha usato il comando '/start'")


def attacchi_rimanenti(update: Update, context: CallbackContext):
    context.bot.send_message(update.message.chat_id,
                             text="Gli attacchi rimanenti in war sono:")
    string = Clash_of_clans.current_war()
    context.bot.send_message(update.message.chat_id,
                             text=string,
                             parse_mode='MarkdownV2')


def staff(update: Update, context: CallbackContext):
    string = Telegram.get_staff()
    context.bot.send_message(update.message.chat_id,
                             text=string,
                             parse_mode='MarkdownV2')


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""Available Commands :
	/attacchi_rimanenti - Scopri quanti attacchi rimangono nella war!""")


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry '%s' is not a valid command" %
                              update.message.text)


def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text("Sorry I can't recognize you , you said '%s'" %
                              update.message.text)


updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(
    CommandHandler('Attacchi_rimanenti', attacchi_rimanenti))
updater.dispatcher.add_handler(CommandHandler('Staff', staff))
updater.dispatcher.add_handler(CommandHandler('help', help))
#updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
#updater.dispatcher.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands

# Start Bot
keep_alive()
updater.start_polling()
