import vk_api
from vk_api.bot_longpoll import VkBotEventType
from core.Config import Config
from core.LongPoll import LongPoll
from core.Callbacks import *
from core.db import db
import schedule

class Bot(object):
    session = None
    api = None
    longpoll = None

    def _init():
        Config.load()

        Bot.session  = vk_api.VkApi(token=Config.token)
        Bot.api      = Bot.session.get_api()
        Bot.longpoll = LongPoll(Bot.session, Config.group_id)

        if Bot.api.groups.getOnlineStatus(group_id=Config.group_id)['status'] == 'none':
            Bot.api.groups.enableOnline(group_id=Config.group_id)

        db.load()
        db.set_yusup_id(Bot.api)
        schedule.every().day.at("10:30").do(run_threaded, job)
        # start_new_thread

    def start():   
        Bot._init()
        schedule.run_pending()
        for event in Bot.longpoll.listen():
            if event.type == VkBotEventType.MESSAGE_NEW:
                OnMessageNew(Bot.api, event)
            elif event.type == VkBotEventType.AUDIO_NEW:
                OnAudioNew(Bot.api, event)
            elif event.type == VkBotEventType.MESSAGE_ALLOW:
                OnMessageAllow(Bot.api, event)
            elif event.type == VkBotEventType.MESSAGE_DENY:
                OnMessageDeny(Bot.api, event)
            else:
                OnDefault(Bot.api, event)            


