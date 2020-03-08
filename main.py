# -*- coding: utf-8 -*-
from threading import Thread
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import telebot
import hendlers
import config

token_tg = config.tg_token
token_vk = config.vk_token
start_message_for = '''Ваше сообщение принято, ожидайте ответа админа'''


class MyThreadVK(Thread):
    """
    A threading example
    """
    bot = telebot.TeleBot(token_tg)
    token = token_vk

    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name

    def run(self):
        # Авторизуемся как сообщество
        vk = vk_api.VkApi(token=self.token)
        # Работа с сообщениями
        longpoll = VkLongPoll(vk)
        # Основной цикл
        for event in longpoll.listen():
            # Если пришло новое сообщение
            if event.type == VkEventType.MESSAGE_NEW:
                # Если оно имеет метку для меня( то есть бота)
                if event.to_me:
                    # Сообщение от пользователя
                    request = event.text
                    # print(request)
                    self.bot.send_message(321107998, request + "  send from: " + str(event.user_id))
                    vk.method('messages.send', {'user_id': event.user_id, 'message': start_message_for})


class MyThreadTG(Thread):
    """
    A threading example
    """

    def __init__(self, name):
        """Инициализация потока"""
        Thread.__init__(self)
        self.name = name

    def run(self):
        hendlers.bot.polling()


def create_threads():
    """
    Создаем группу потоков
    """
    my_thread_vk = MyThreadVK("Vk")
    my_thread_vk.start()
    my_thread_tg = MyThreadTG("Telegram")
    my_thread_tg.start()


if __name__ == "__main__":
    create_threads()
