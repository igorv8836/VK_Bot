import vk_api
import bs4
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from MessageClass import MessageClass

def main():
    key_access = 'vk1.a.El5OgrYlMPQrrFUIdR5EdvbaU8vBDXZNz7j73k0usi' \
                 '-BGZZNIkl4gfMGEGOIv5QNT9V1ZmbSA3eCbAOniq6xEZWhwFLjvDzf1Yz' \
                 '-1w72AdXoNNwPIQCUdDSKhSQPrIENKBo0Ty_ashR62IijoFygWIXKpeYHEtRk1em2Z6Ow-_YpDHDadEPvY5CPidWkXly9' \
                 '-C91kvJLp9eRPD67zOdwPg'
    vk_session = vk_api.VkApi(token=key_access)
    longpoll = VkLongPoll(vk_session)

    def send_message(user_id, message, random_id=0):
        vk_session.method('messages.send',
                          {'user_id': user_id, 'message': message, 'random_id': random_id})

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            u_id = event.user_id

            if event.text == 'Начать':
                send_message(u_id, MessageClass.FIRST_MESSAGE)
                print(123)
            send_message(u_id, f'Вы написали: {event.text}', 1)


main()
