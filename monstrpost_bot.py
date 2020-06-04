from datetime import datetime, timedelta
import telebot
from telebot import types
import requests
import schedule
import threading
import time

import re
import os


API_TOKEN = '1215464937:AAH_-Sk9KggqSQdb1_rdTJldGgKZtMUxrbw'
bot = telebot.TeleBot(API_TOKEN)


#@bot.message_handler(commands=['start', 'help'])
@bot.message_handler(func=lambda message: message.text == 'Привет')
def send_welcome(message):

    bot.send_message(message.chat.id,text='Я - Трекер цены BIP за BTC.Ориентируюсь по биржe BITEX.')

def send_price_bitex():

    URL_BIP_COST='https://blockchain.info/ticker'
    payload = {'getOrders': 1,'token': 'BTC','authkey': 'IOOnhg678TRrfvvvbhujk987TybnbFGtBBVfooe45ds7756GVCFbbnngg5467YHnHgFDG'}
    URL='https://bipex.net/dex/ajax.php'
    r_url=requests.get(URL_BIP_COST)
    r = requests.post(URL, data=payload)
    amount=0
    amount2=0
    sell_btc=[]
    buy_btc=[]
    cost_btc=r_url.json()['USD']['15m']

    for i in r.json()['SELL']['BTC']:
        amount+=1
        sell_btc.append(i)

    for i in r.json()['BUY']['BTC']:
        amount2+=1
        buy_btc.append(i)

    min_buy_cost=float(max(buy_btc))*float(cost_btc)
    min_sell_cost=float(min(sell_btc))*float(cost_btc)

    bot.send_message(chat_id="@MonstersBIPprice",text='📉'+str(round(min_buy_cost,4))+' $ / 📈'+str(round(min_sell_cost,4))+'$')


def schedule_d():
    while 1:
        schedule.run_pending()
        time.sleep(1)

thread2 = threading.Thread(target=schedule_d)
thread2.start()

schedule.every(1).minutes.do(send_price_bitex)
do=send_price_bitex()


bot.polling(none_stop=True, interval=0)
