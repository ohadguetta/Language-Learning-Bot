import time
import logging
# import re
# import datetime
import json

from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler,
)

logging.basicConfig(  # if things not working properly
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


BOT_TOKEN = '6446448924:AAEWPivNKmRfsEdYVy0MZLKryOCD08fblPM' #DONE: add bot token
DEFAULT_MESSAGE = 'Welcome to the Language Learner bot 🇮🇱! \n <b>Pick a language to learn:</b>'



#async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
#    await context.bot.send_message(chat_id=update.effective_chat.id, text=messageToSend)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text=f'Hebrew 🇮🇱',callback_data=json.dumps({'language':'Hebrew'}))],
        [InlineKeyboardButton("Spanish 🇪🇸", callback_data=json.dumps({'language': 'Spanish'}))],
    ]

    markup_languages = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id, text=DEFAULT_MESSAGE,
        reply_markup= markup_languages,
        parse_mode=ParseMode.HTML
    )

async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Handle button clicks here
    data = json.loads(query.data)
    chosen_language = data['language']
    #TODO: subscribe user to word of the day in firebase firestore
    #TODO: send the user a word of the day every day
    await query.edit_message_text(text=f"You Clicked {chosen_language}")



if __name__ == "__main__":
    application = (
        ApplicationBuilder()
        .token(BOT_TOKEN)
        .build()
    )



    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))

    # application.add_handler(CommandHandler("archivereminders", archiveReminders))



    # job_queue = application.job_queue

    # job_minute = job_queue.run_repeating(checkReminders, interval=20, first=10)

    application.run_polling()