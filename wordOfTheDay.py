import logging
import firebase_admin
from firebase_admin import credentials, firestore,exceptions
# from translate import Translator
# from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


# Replace with your Firebase credentials JSON file
cred = credentials.Certificate("serviceAccountKey.json") #DONE: add firebase firestore
firebase_admin.initialize_app(cred)
db = firestore.client()

logging.basicConfig(  # if things not working properly
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

def subscribe_user(user_id,language):
    try:
        user_ref = db.collection('users').document(str(user_id))
        # print(user_ref.get().to_dict())
        if user_ref.get().exists:
            user_ref.update({'subscriptions': firestore.ArrayUnion([language]) }) #DONE: check if user already subscribed before addition of language
        else:
            user_ref.set({'subscriptions': firestore.ArrayUnion([language]) }) 
        return True
    except exceptions.FirebaseError as e:
        logging.warning('Server has returned an error',e)
        return False



# def send_word_of_the_day():
#     # Fetch the word of the day from your source
#     word_of_the_day = 'YourWordOfTheDay'

#     # Send the word of the day to the subscribed users
#     db = firestore.client()
#     subscribed_users_ref = db.collection('subscribed_users').where('subscribed', '==', True).stream()

#     # bot = Updater(TELEGRAM_BOT_TOKEN).bot

#     for user in subscribed_users_ref:
#         user_id = user.id
#         try:
#             bot.send_message(chat_id=user_id, text=f"Word of the Day: {word_of_the_day}")
#         except Exception as e:
#             print(f"Error sending message to user {user_id}: {e}")


def pull_subscriptions():
    subscriptions_ref = db.collection('users').where('subscriptions', '!=', []).stream()
    subscribed_users = []

    for user in subscriptions_ref:
        user_data = user.to_dict()
        chat_id = user.id
        subscribed_users.append({'chat_id': chat_id, 'subscriptions': user_data.get('subscriptions', [])})
    
    return subscribed_users

def getRandomWord(language):
    #TODO: get random word and return its translation to the languagea and the word itself
    # translator= Translator(to_lang="eng")
    # translation = translator.translate('לקחת')
    if language == 'Hebrew':
        # return {'word':{translation},'translation':'לקחת'}
        return {'word':'Take','translation':'לקחת'}
    elif language =='Spanish':
        return {'word':'Take','translation':'llevar'}