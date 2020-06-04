from datetime import datetime, timedelta
import telebot
from telebot import types
import requests
import schedule
import threading
import time

import re
import os


API_TOKEN = '1203771892:AAGWkhDc-JxdSaKMDb30V-vXipaSPdG5IpQ'
bot = telebot.TeleBot(API_TOKEN)


#@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: message.text == 'Привет')
def send_welcome(message):

    bot.send_message(message.chat.id,text='Я - Трекер цены BIP за BTC.Ориентируюсь по бирже BithumbGlobal.')

def get_bithump_price():

    URL_BIP_COST_BITHUMP='https://global-openapi.bithumb.pro/market/data/ticker?symbol=BIP-USDT'
    bithump_url=requests.get(URL_BIP_COST_BITHUMP)
    sell_usdt=[]
    buy_usdt=[]
    data = bithump_url.json()['info'][0]

    return(data)


def send_price_bithumb():

    cost = get_bithump_price();
    price = round((float(cost['c'])),6)
    bot.send_message(chat_id="@bipprice",text=str(price) + ' $')


def schedule_d():
    while 1:
        schedule.run_pending()
        time.sleep(1)

thread3 = threading.Thread(target=schedule_d)
thread3.start()

schedule.every(1).minutes.do(send_price_bithumb)
do=send_price_bithumb()

bot.polling(none_stop=True, interval=0)
