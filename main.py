import time
import logging

# import re
# import datetime
import json
import wordOfTheDay

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


BOT_TOKEN = "6446448924:AAEWPivNKmRfsEdYVy0MZLKryOCD08fblPM"  # DONE: add bot token
DEFAULT_MESSAGE = "Welcome to the Language Learner bot 🇮🇱! \n <b>Pick a language to learn:</b>"
languages = ['Hebrew','Spanish']


# async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):

#    await context.bot.send_message(chat_id=update.effective_chat.id, text=messageToSend)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(text=f'Hebrew 🇮🇱',callback_data=json.dumps({'language':'Hebrew'}))],
        [InlineKeyboardButton(text="Spanish 🇪🇸", callback_data=json.dumps({'language': 'Spanish'}))]
    ]
    markup_languages = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=DEFAULT_MESSAGE,
        reply_markup=markup_languages,
        parse_mode=ParseMode.HTML
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    # Handle button clicks here
    data = json.loads(query.data)
    chosen_language = data["language"]
    # DONE: subscribe user to word of the day in firebase firestore
    # TODO: send the user a word of the day every day
    isSuccess = wordOfTheDay.subscribe_user(update.effective_chat.id, chosen_language)

    if isSuccess:
        await query.edit_message_text(
            text=f"You subscribed successfully to the {chosen_language} language!"
        )
    else:
        await query.edit_message_text(text=f"There was an error in the server!")




async def send_wotd(update: Update,context: ContextTypes.DEFAULT_TYPE): #Sends word of the day to all users
    wotdArr = {}
    for language in languages:
        wotdArr[language] = wordOfTheDay.getRandomWord(language)
    subscribed_users = wordOfTheDay.pull_subscriptions()
    for user in subscribed_users: #TODO: check for every user and its languages and send its word of the day
        for language in user['subscriptions']:
            try:
                await context.bot.send_message(
                chat_id= user['chat_id']
                ,text=f'Translation to <b>{wotdArr[language]["word"]}</b> in {language} is: <b>{wotdArr[language]["translation"]}</b>' #DONE: add word of the day
                # reply_markup= #TODO: maybe add a list of known words to user
                ,parse_mode=ParseMode.HTML
                )
            except:
                logging.warning('Error when sending wotd,user not found probably')
    
async def pull_subscriptions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = wordOfTheDay.pull_subscriptions()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=result, 
    )







if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("send_word_of_the_day", send_wotd))
    application.add_handler(CommandHandler("pull_subscriptions", pull_subscriptions))
    application.add_handler(CallbackQueryHandler(button_click))

    # application.add_handler(CommandHandler("archivereminders", archiveReminders))

    # job_queue = application.job_queue

    # job_minute = job_queue.run_repeating(checkReminders, interval=20, first=10)

    application.run_polling()
