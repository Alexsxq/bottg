from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Безопасно!

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Бот работает! 🚀")

updater = Updater(BOT_TOKEN)
updater.dispatcher.add_handler(CommandHandler("start", start))
updater.start_polling()
updater.idle()
