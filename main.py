import os

from telegram.ext import CallbackContext, Application, ContextTypes
from telegram.ext import CommandHandler
from telegram.ext import Updater
from telegram import Update
from webserver import keep_alive
from settings.telegram import Telegram
from settings.clash_of_clans import Clash_of_clans

BOT_TOKEN = os.environ['Bot_token']
COC_TOKEN = os.environ['Clash_of_clans_API_token']

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    print("L'utente " + str(user) + " ha usato il comando '/start'")


async def attacchi_rimanenti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(update.message.chat_id,
                             text="Gli attacchi rimanenti in war sono:")
    string = Clash_of_clans.current_war()
    context.bot.send_message(update.message.chat_id,
                             text=string,
                             parse_mode='MarkdownV2')


async def risultati_ultima_war(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.bot.send_message(update.message.chat_id,
                             text="Risultati della war:")
    string = Clash_of_clans.result_last_war()
    context.bot.send_message(update.message.chat_id,
                             text=string,
                             parse_mode='MarkdownV2')


async def staff(update: Update, context: ContextTypes.DEFAULT_TYPE):
    string = Telegram.get_staff()
    context.bot.send_message(update.message.chat_id,
                             text=string,
                             parse_mode='MarkdownV2')


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""Available Commands :
	/attacchi_rimanenti - Scopri quanti attacchi rimangono nella war!""")


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    string = Telegram.info()
    await context.bot.send_message(update.message.chat_id,
                             text=string)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry '%s' is not a valid command" %
                                    update.message.text)


async def unknown_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Sorry I can't recognize you , you said '%s'" %
                                    update.message.text)


# Start Bot
if __name__ == '__main__':
    print('Starting bot...')
    app = Application.builder().token(BOT_TOKEN).build()

    #Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('Attacchi_rimanenti', attacchi_rimanenti))
    app.add_handler(CommandHandler('Risultati_ultima_war', risultati_ultima_war))
    app.add_handler(CommandHandler('Staff', staff))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('help', help))
    # app.add_handler(MessageHandler(Filters.text, unknown))
    # app.add_handler(MessageHandler(Filters.command, unknown))  # Filters out unknown commands


    #Bot started
    #keep_alive()
    print('Polling...')
    app.run_polling(1.0)
    #updater.start_polling()
