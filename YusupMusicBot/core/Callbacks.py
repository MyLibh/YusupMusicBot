import json
import os
from vk_api.utils import get_random_id
from core.BotKeyboard import BotKeyboard
from core.db import db
from core.Util import *
from core.Config import Config

def _handle_chat_message():
    return

def _handle_user_message(api, text, user, msg_id, attachments):
    if text == 'Music🎵':
        if os.path.exists('data/songs.json'):
            with open('data/songs.json', 'r', encoding='utf-8') as file:
                data = json.loads(file.read())
                
                api.messages.send(user_id=user, message='Последние добавленные:', attachment=data, reply_to=msg_id, random_id=get_random_id())
                # random song ?
        else:                
            api.messages.send(user_id=user, message='Песни не нашлось(', reply_to=msg_id, random_id=get_random_id())
    elif text.lower() == 'start' or text.lower() == 'начать':
        if user == db.yusup_id:
            BotKeyboard.send_menu_keyboard(api, user, perms=1)
        else:
            BotKeyboard.send_menu_keyboard(api, user)
        db.add_user(user)
    elif user == db.yusup_id:
        if text == 'Add':
            _handle_user_message.last_act = 1
            api.messages.send(user_id=user, message='Добавляй!', reply_to=msg_id, random_id=get_random_id())
        elif text == 'Send':
            _handle_user_message.last_act = 2
            api.messages.send(user_id=user, message='Что отослать?', reply_to=msg_id, random_id=get_random_id())
        elif _handle_user_message.last_act == 1:
            if os.path.exists('data/songs.json'):
                with open('data/songs.json', 'r', encoding='utf-8') as file:
                    data = json.loads(file.read())
            for x in attachments:
                data.append(x)
            with open('data/songs.json', 'w+', encoding='utf-8') as file:
                try:
                    file.write(unicode(json.dumps(data, ensure_ascii=False, indent=4)))
                except NameError:
                    file.write(str(json.dumps(data, ensure_ascii=False, indent=4)))
            api.messages.send(user_id=user, message='Добавил', reply_to=msg_id, random_id=get_random_id())
            _handle_user_message.ast_act = 0
        elif _handle_user_message.last_act == 2:
            if len(text) == 0:
                text = 'Новая песня!'
            for user in db.users:
                if user != db.yusup_id:
                    api.messages.send(user_id=user, message=text, attachment=attachments, random_id=get_random_id())
            api.messages.send(user_id=user, message='Отослал', reply_to=msg_id, random_id=get_random_id())
            _handle_user_message.ast_act = 0
_handle_user_message.last_act = 0

def OnMessageNew(api, event):
    user = event.obj.from_id
    text = event.obj.text
    attachments = event.obj.attachments
    msg_id = event.obj.id

    if event.from_chat:
        _handle_chat_message()
    elif event.from_user:
        _handle_user_message(api, text, user, msg_id, get_attachs(attachments))

def OnAudioNew(api, event):
    for user in db.users:
            api.messages.send(user_id=user, message='Новая песня в группе!', attachment='audio' + str(event.obj.owner_id) + '_' + str(event.obj.id), random_id=get_random_id())

def OnMessageAllow(api, event):
    db.add_user(event.user_id)

def OnMessageDeny(api, event):
    db.remove_user(event.user_id)

def OnDefault(api, event):
    return