import os
import time

import requests
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

ACCOUNT_SID = os.getenv('ACCOUNT_SID')
AUTH_TOKEN = os.getenv('AUTH_TOKEN')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')
VK_TOKEN = os.getenv('VK_TOKEN')
VK_API_URL = 'https://api.vk.com/method/users.get'
VERSION = '5.92'


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'fields': 'online',
        'access_token': VK_TOKEN,
        'v': VERSION,
    }
    status = requests.post(
        VK_API_URL, params=params
    ).json()['response'][0]['online']
    return status


def sms_sender(sms_text):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input("Введите id ")
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(15)
