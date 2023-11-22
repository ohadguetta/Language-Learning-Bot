import logging
import firebase_admin
from firebase_admin import credentials, firestore,exceptions

import random
import json


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



def pull_subscriptions():
    subscriptions_ref = db.collection('users').where('subscriptions', '!=', []).stream()
    subscribed_users = []

    for user in subscriptions_ref:
        user_data = user.to_dict()
        chat_id = user.id
        subscribed_users.append({'chat_id': chat_id, 'subscriptions': user_data.get('subscriptions', [])})
    
    return subscribed_users

def getRandomWord(language):
    #DONE: get random word and return its translation to the languagea and the word itself
    with open(f'{language.lower()}Words.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    random_entry = random.choice(data)
    return random_entry