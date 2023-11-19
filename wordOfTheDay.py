import firebase_admin
from firebase_admin import credentials, firestore
# from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters


# Replace with your Firebase credentials JSON file
cred = credentials.Certificate("path/to/your/firebase-credentials.json") #TODO: add firebase firestore
firebase_admin.initialize_app(cred)

db = firestore.client()

def subscribe_user(user_id,language):
    user_ref = db.collection('users').document(str(user_id))
    user_ref.set({'subscriptions': firestore.ArrayUnion([language]) }) #TODO: check if user already subscribed before addition of language
    


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
        user_id = user.id
        subscribed_users.append({'user_id': user_id, 'language': user_data.get('subscribed_languages', [])})
    
    return subscribed_users