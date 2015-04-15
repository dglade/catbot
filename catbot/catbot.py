import hipchat
import random
import time
import settings
from datetime import datetime

def randomize(max_index):
    random.seed()
    return random.randint(0, max_index)

def speak(hc, room, message):
    hc.message_room(room,
                    settings.SENDER_NAME,
                    message,
                    color=settings.MESSAGE_COLOR)

def lurk():
    hc = hipchat.HipChat(token=settings.ADMIN_API_TOKEN)
    prior_messages = []
    while True:
        random_room = settings.ROOMS_LIST[randomize(len(settings.ROOMS_LIST) - 1)]
        random_message = settings.MESSAGE_LIST[randomize(len(settings.MESSAGE_LIST) - 1)]
        print("room: {}, message: {}".format(random_room, random_message))
        history = hc.method('rooms/history',
                            method='GET',
                            parameters={'room_id': random_room,
                                        'date': str(datetime.date(datetime.now()))})
        if len(history['messages']) > 0 and \
                history['messages'] != prior_messages and \
                history['messages'][-1]['from']['name'] in settings.USERS_TO_FOLLOW:
            speak(hc, random_room, random_message)
        time.sleep(settings.SLEEP_INTERVAL)
        prior_messages = history['messages']

if __name__ == '__main__':
    lurk()

