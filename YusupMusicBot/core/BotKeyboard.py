from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id

class BotKeyboard(object):
    def send_menu_keyboard(api, user_id, msg='Добрый вечер)', perms=0):
        keyboard = VkKeyboard(one_time=False)

        if perms != 0:
            keyboard.add_button('Add', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()
            keyboard.add_button('Send', color=VkKeyboardColor.PRIMARY)
            keyboard.add_line()

        keyboard.add_button(u'Music🎵', color=VkKeyboardColor.POSITIVE)

        api.messages.send(peer_id=user_id, random_id=get_random_id(), keyboard=keyboard.get_keyboard(), message=msg)
