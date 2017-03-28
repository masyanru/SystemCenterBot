#! /usr/bin/env python
# -*- coding: utf-8 -*-

import configparser

from datetime import datetime, timedelta
import telebot
import feedparser

"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
"""

# создание бота с его токеном API и подгружаем конфиг
config = configparser.ConfigParser()
config.read("config.ini")
bot = telebot.TeleBot(config["Telegram"]["access_token"])


def auto_posting():
    bot.send_message('-179710499', 'Test')


RSS_URLS = [
    'http://masyan.ru/feed/'

]


"""
    'http://ccmexec.com/feed/',
    'https://blogs.technet.microsoft.com/enterprisemobility/feed/',
    'https://blogs.technet.microsoft.com/configurationmgr/feed/',
    'https://www.enhansoft.com/feed',
    'http://windowsmanagementexperts.com/feed/',
    'http://systemcenterme.com/?feed=rss2',
    'http://liashov.com/?feed=rss2',
    'https://www.systemcenterdudes.com/feed/',
    'https://skatterbrainz.wordpress.com/feed/',
    'http://wmug.co.uk/wmug/rss'
    """


feeds = []
for url in RSS_URLS:
    feeds.append(feedparser.parse(url))

rss = []
lastHourDateTime = datetime.today() - timedelta(hours=48)

for feed in feeds:
    title = feed['entries'][0].title
    url = feed['entries'][0].link
    date_p = feed['entries'][0].updated
    t = datetime.strptime(date_p[0:25], "%a, %d %b %Y %H:%M:%S")
    # print('convert t', t)
    # print('Дата в посте: ', date_p)
    # print('- 24 часа', lastHourDateTime)
    # print('Сегодня', datetime.today())
    if t > lastHourDateTime:
        rss.append(title + ' ' + url + '\n\n')
        print(title + ' ' + url)

    else:
        print('Пусто')


if rss is not None:
    print('Rss is empty')
    # sccm channel
    # bot.send_message('-1001054149356',  "Configuration Manager news: \n\n" + "".join(rss), parse_mode="Markdown", disable_web_page_preview=True)
    # test channel
    bot.send_message('-179710499', "Чот нет новостей, беда, печаль!")
else:
    # sccm channel
    # bot.send_message('-1001054149356',  "Configuration Manager news: \n\n" + "".join(rss), parse_mode="Markdown", disable_web_page_preview=True)
    # test channel
    bot.send_message('-179710499', "Configuration Manager news: \n\n" + "".join(rss), parse_mode="Markdown",
                     disable_web_page_preview=True)
    # bot.send_message('-179710499', title + ' ' + url, disable_web_page_preview=True)
