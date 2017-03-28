#! /usr/bin/env python
# -*- coding: utf-8 -*-

import schedule
import urllib
import time
from datetime import datetime

import telebot  # подключение библиотеки pyTelegramBotAPI
import logging  # библиотека журнала
import random
import feedparser
import configparser

"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
"""

# настройки для журнала
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('someTestBot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)

# создание бота с его токеном API и подгружаем конфиг
config = configparser.ConfigParser()
config.read("config.ini")
bot = telebot.TeleBot(config["Telegram"]["access_token"])

# текст справки
help_string = []
help_string.append("Справка по командам System Center бота.\n\n")
help_string.append("/start - выводит приветствие\n")
help_string.append("/help - отображает эту справку\n")
help_string.append("/feed - парсер RSS (в процессе ...)\n")
help_string.append("Больше пока нет, терпение. Версия 0.2\n")

# hello сообщения


text_messages = {
    'welcome':
        u'{name}, добро пожаловать на канал.\n'
        u'Тут бывает много сообщений + из-за разницы в часовых поясах они могут приходить оооочень рано, так что отключай нотификации в свойствах этого телеграм чата, чтобы не просыпаться от группового траблшутинга в 5 утра по Москве.\n'
        u'FB - https://www.facebook.com/groups/sccm.russia/\n'
        u'SCCM - https://telegram.me/ConfigMgr\n'
        u'SCOM - https://telegram.me/OpsMgr\n'
        u'IT Talks для общих тем - https://telegram.me/ITtalks\n'
        u'Новостной канал - https://telegram.me/MicrosoftRus\n'
        u'Подписываемся.\n',

    'info':
        u'My name is Bot,\n',

    'wrong_chat':
        u'Hi there!\nThanks for trying me out.',

    'vzzz':
        ".∧＿∧ \n"
        "( ･ω･｡)つ━☆・*。\n"
        "⊂  ノ    ・゜+.\n"
        "しーＪ   °。+ *´¨)\n"
        "         .· ´¸.·*´¨) ¸.·*¨)\n"
        "          (¸.·´ (¸.·'* ☆"

}


@bot.message_handler(func=lambda m: True, content_types=['new_chat_member'])
def on_user_joins(message):
    name = message.new_chat_member.first_name
    name += u" (@{})".format(message.new_chat_member.username)

    # bot.reply_to(message, text_messages['welcome'].format(name=name))
    # bot.send_message(message.chat.id, "Bot send message.")
    bot.send_message(message.chat.id, text_messages['welcome'].format(name=name), disable_web_page_preview=True)


# @bot.message_handler(func=lambda message: message.text == "1")
@bot.message_handler(func=lambda message: message.text.__contains__('не знаю'))
def echo_dont_know(message):
    bot.send_message(message.chat.id, '¯\_(ツ)_/¯')


@bot.message_handler(func=lambda message: message.text.__contains__('вжух'))
def echo_vzzz(message):
    bot.send_message(message.chat.id, text_messages['vzzz'])


@bot.message_handler(func=lambda message: message.text.__contains__('заебись'))
def send_zbs(message):
    #
    # name = message.first_name
    random_text = ["Готово!", "Будет сделано!", "Давай завтра сделаем, {name}, а?",
                   "{name}, тебе надо - ты и делай!", "Я уже делал заебись.", "Кстати, в прошлый раз получилось лучше.",
                   "Получилось!", "Заебись!", "Иди на течнет", "Я бы сделал, да мне лень.",
                   "Ухаха, то есть мяу!", "{name}, я сделал!", "Я сделаль!", "Вжух и все заебись!",
                   "На скилле затащил и сделал",
                   "Я вам тут все клево ща сделаю", "Думаешь я бот? Нет, я просто делаю сразу збс",
                   "Нормально делай, нормально будет!", "Хуякс, хуякс и в продакшен!",
                   "Давай ты сначала поселектишь в базу, а потом сделаем збс",
                   "Обновись и будет збс", "А ты апдейты давно ставил?", "shutdown -r -t 0", "Вжух, вжух и в продакшен"
                   ]
    # uname = message.from_user.first_name

    # bot.reply_to(message, random.choice(random_text).format(name=uname))
    uname = u"@{}".format(message.from_user.username)
    bot.send_message(message.chat.id, random.choice(random_text).format(name=uname))


@bot.message_handler(func=lambda message: message.text.__contains__('пиздец'))
def send_pizdec(message):
    #
    # name = message.first_name
    random_text = ["А я знал, что так и будет", "Не унывай, ну ты чо.", "Сам такой, {name}.",
                   "{name}, не ругайся!", "Ага, тот еще пиздец!"

                   ]
    uname = u"@{}".format(message.from_user.username)
    bot.send_message(message.chat.id, random.choice(random_text).format(name=uname))


@bot.message_handler(func=lambda message: message.text == "+")
def rating(message):


# --- команды


@bot.message_handler(commands=['start'])
def send_start(message):
    #
    bot.send_message(message.chat.id, "Привет, я System Center бот! Отправьте мне /help для вывода справки.")


@bot.message_handler(commands=['help'])
def send_help(message):
    #
    bot.send_message(message.chat.id, "".join(help_string), parse_mode="Markdown")


@bot.message_handler(commands=['feed'])
def send_feed(message):
    url = feedparser.parse('http://masyan.ru/feed/')
    # title = url['entries'][1].title
    # description = url['entries'][1].summary
    # rssurl = url['entries'][1].link

    bot.send_message(message.chat.id, url['entries'][0].link)


# запуск приёма сообщений
if __name__ == '__main__':
    bot.polling(none_stop=True)