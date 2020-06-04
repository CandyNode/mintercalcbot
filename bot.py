from datetime import datetime, timedelta
#from bithumb_api.BithumbGlobal import *
from pycoingecko import CoinGeckoAPI
from PIL import Image, ImageDraw, ImageFont
import telebot
from telebot import types
import requests
import datetime
import schedule
import threading
import time
import re
import os

API_TOKEN = '1246762966:AAFuLymjGfY6McoHYU4dPsgaIPUUSJCyI1o'
bot = telebot.TeleBot(API_TOKEN)
cwd = os.getcwd()
cg = CoinGeckoAPI()
bignumber = 10000000001

#@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda message: message.text == 'Привет')
def send_welcome(message):

    bot.send_message(message.chat.id,text='Скорость превыше всего! Бот, который экономит время.\n\nКалькулятор цены BIP и других криптовалют в любом чате\n\n- Напишите 1 POPE или 10 BTC и я покажу вам актуальный курс монеты.\n\n- Введите Price для получения детальной статистики по монете BIP')

@bot.message_handler(commands=['picture', 'pic'])
@bot.message_handler(func=lambda message: message.text == 'pic')
@bot.message_handler(func=lambda message: message.text == 'pic')
@bot.message_handler(func=lambda message: message.text == 'Picture')
@bot.message_handler(func=lambda message: message.text == 'Pic')

def send_picture_bithumb(message):

    currentDT = datetime.datetime.now()
    currentdate = currentDT.strftime("%a, %b %d, %Y")
    currentdatevar = currentDT.strftime("%Y-%m-%d %H:%M:%S")

    cost = get_bithump_price()
    price = str(round(float(cost['c']),6))
    percent_pic = round((float(cost['p'])*100),4)
    percent = str(round((float(cost['p'])*100),4))
    vol = str(round(float(cost['vol']),4))
    highest = float(cost['h'])
    lowest = float(cost['l'])
    units = float(cost['v'])

    filename = "assets/pic/image.png"

    image = Image.open('assets/pic/bithumb_var.jpg')
    draw = ImageDraw.Draw(image)

    if(percent_pic>0):
        background = Image.open('assets/pic/green.png').convert("RGBA")
    else:
        background = Image.open('assets/pic/red.png').convert("RGBA")


    image.paste(background,(0,0),background)
    font = ImageFont.truetype('assets/fonts/onemore.otf', size=85)
    (x, y) = (210, 75)
    name = 'BIP'
    color = 'rgb(255, 255, 255)'
    draw.text((x, y), name, fill=color, font=font)
    #Цена
    font_price = ImageFont.truetype('assets/fonts/DMMono-Regular.ttf', size=65)
    (x, y) = (120, 160)
    draw.text((x, y), '$ '+price , fill=color,font=font_price)
    #Вверх/Вниз
    font_percent = ImageFont.truetype('assets/fonts/DMMono-Regular.ttf', size=45)
    (x, y) = (250, 240)
    draw.text((x, y), percent + ' %' , fill=color,font=font_percent)
    #Ссылка
    font_30 = ImageFont.truetype('assets/fonts/DMMono-Regular.ttf', size=30)
    #(x, y) = (40, 300)
    #name = 'https://t.me/CandyNode'
    #color = 'rgb(255, 255, 255)'
    #draw.text((x, y), name, fill=color, font=font_30)
    #Дата
    (x, y) = (170, 10)
    name = str(currentdate)
    draw.text((x, y), name, fill=color, font=font_30)
    #Объем
    (x ,y) = (120,320)
    draw.text((x, y), '24H Vol: '+vol + ' USDT', fill=color, font=font_30)
    image.save(filename)
    os.system(filename)
    photo = open('assets/pic/image.png', 'rb')
    bot.send_photo(chat_id=message.chat.id, photo=photo)

@bot.message_handler(commands=['price'])
@bot.message_handler(func=lambda message: message.text == 'Цена')
@bot.message_handler(func=lambda message: message.text == 'Price')
@bot.message_handler(func=lambda message: message.text == 'price')
@bot.message_handler(func=lambda message: message.text == 'Стоимость')
def send_priceonetime(message):
    cost = get_bithump_price();
    price = float(cost['c'])
    percent = round((float(cost['p'])*100),4)
    vol = place_value(round(float(cost['vol']),4))
    highest = float(cost['h'])
    lowest = float(cost['l'])
    units = place_value(float(cost['v']))
    text = '\n\n<b>BIP/USDT Data</b>\n\n<b>💰 Price:</b> ' + '<pre>'+str(price) + ' USDT</pre>' +'\n<b>💰 24H Change:</b> ' + '<code>'+str(percent) + '%</code>'  + '\n\n<b>📉 Low:</b> ' + '<code>'+str(lowest) +' USDT</code>' + '\n<b>📈 High:</b> ' +'<code>'+str(highest) + ' USDT</code>' + '\n\n<b>📊 24H Units:</b> ' + '<code>'+str(units) + ' BIP</code>' + '\n<b>📊 24H Vol:</b> ' +'<code>'+str(vol) +' USDT</code>' + '\n\n<i>by Bithumb Global</i>'
    bot.send_message(chat_id=message.chat.id,text=text,parse_mode="html")

def place_value(number):

    return ("{:,}".format(number).replace(',', ' '))

def get_bithump_price():

    URL_BIP_COST_BITHUMP='https://global-openapi.bithumb.pro/market/data/ticker?symbol=BIP-USDT'
    bithump_url=requests.get(URL_BIP_COST_BITHUMP)
    sell_usdt=[]
    buy_usdt=[]
    data = bithump_url.json()['info'][0]

    return(data)


@bot.message_handler(commands=['gechoprice'])
@bot.message_handler(func=lambda message: message.text == 'Цена Coingecho')
@bot.message_handler(func=lambda message: message.text == 'Price Coingecho')
@bot.message_handler(func=lambda message: message.text == 'Стоимость Coingecho')
def send_pricegecho(message):

    btc_price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    eth_price = cg.get_price(ids='ethereum', vs_currencies='usd')
    bip_price = cg.get_price(ids='bip', vs_currencies='usd')

    all_prices = '🥇 BTC: '+ str(btc_price['bitcoin']['usd'])+' 💰 \n💨 ETH: '+ str(eth_price['ethereum']['usd'])+' 💰 \nⓂ️ BIP: ' + str(bip_price['bip']['usd']) + ' 💰'
    bot.send_message(chat_id=message.chat.id,text=all_prices)



def coins_list():

    explorer_url = 'https://explorer-api.minter.network/api/v1/coins'
    r = requests.get(explorer_url)
    coins_list = []

    for i in r.json()['data']:
        coins_list.append(i['symbol'])

    return coins_list

def coingecko_list():

    coingecko_list = cg.get_coins()
    allgecko_list = []

    for i in coingecko_list:
        allgecko_list.append(i['symbol'])

    return allgecko_list


def get_balance_bip():
    coin = 'BIP'
    balance_bit_url = 'http://api.minter.one/estimate_coin_sell?coin_to_sell='+coin+'&coin_to_buy=BIT&value_to_sell=1000000000000000000'
    r_bit = requests.get(balance_bit_url)
    price_bit = float((r_bit.json()['result']['will_get']))/1000000000000000000

    return price_bit

def get_balance_bip_full(number):
    price = str(int(number * 1000000000000000000))
    balance_bit_url = 'http://api.minter.one/estimate_coin_sell?coin_to_sell=BIP&coin_to_buy=BIT&value_to_sell='+price
    r_bit = requests.get(balance_bit_url)
    price_bit = int((r_bit.json()['result']['will_get']))/1000000000000000000

    return round(price_bit,6)

def get_balance_bit():
    coin = 'BIT'
    balance_bip_url = 'http://api.minter.one/estimate_coin_sell?coin_to_sell='+coin+'&coin_to_buy=BIP&value_to_sell=1000000000000000000'
    r_bip = requests.get(balance_bip_url)
    price_bip = int((r_bip.json()['result']['will_get']))/1000000000000000000

    return price_bip

def get_balance_bit_full(number):
    price = str(int(number * 1000000000000000000))
    balance_bip_url = 'http://api.minter.one/estimate_coin_sell?coin_to_sell=BIT&coin_to_buy=BIP&value_to_sell='+price

    r_bip = requests.get(balance_bip_url)
    price_bip = int((r_bip.json()['result']['will_get']))/1000000000000000000

    return price_bip

def get_balance(coin):

    balance_bip_url = 'http://api.minter.one/estimate_coin_sell?coin_to_sell='+coin+'&coin_to_buy=BIP&value_to_sell=1000000000000000000'
    balance_bit_url = 'http://api.minter.one/estimate_coin_sell?coin_to_sell='+coin+'&coin_to_buy=BIT&value_to_sell=1000000000000000000'
    r_bip = requests.get(balance_bip_url)
    r_bit = requests.get(balance_bit_url)

    if 'result' not in r_bip.json() or 'result' not in r_bit.json():

        price_bip = 'error'
        price_bit = 'error'
        return (price_bip,price_bit)

    else:

        price_bip = int((r_bip.json()['result']['will_get']))/1000000000000000000
        price_bit = int((r_bit.json()['result']['will_get']))/1000000000000000000

        if(price_bip > 1):

            return ((round(price_bip,1)), price_bit)

        else:

            return ((round(price_bip,6)), price_bit)

def get_balance_full(number,coin):
    price = str(int(number * 1000000000000000000))

    balance_bip_url = 'http://api.minter.one/estimate_coin_sell?coin_to_sell='+coin+'&coin_to_buy=BIP&value_to_sell='+price
    balance_bit_url = 'http://api.minter.one/estimate_coin_sell?coin_to_sell='+coin+'&coin_to_buy=BIT&value_to_sell='+price
    r_bip = requests.get(balance_bip_url)
    r_bit = requests.get(balance_bit_url)

    if 'result' not in r_bip.json() or 'result' not in r_bit.json():
        price_bip = 'error'
        price_bit = 'error'

        return (price_bip,price_bit)

    else:

        price_bip = int((r_bip.json()['result']['will_get']))/1000000000000000000
        price_bit = int((r_bit.json()['result']['will_get']))/1000000000000000000

        if(price_bip > 1):

            return ((round(price_bip,1)), price_bit)

        else:

            return ((round(price_bip,6)), price_bit)

def get_gecho_balance(coin):
    coingecko_list = cg.get_coins()
    for i in coingecko_list:
        if(i['symbol'] == coin):
            id = i['id']
    price_coin_usd = cg.get_price(id,'usd')[id]['usd']

    return float(price_coin_usd)

def gecho_calc(number,coin):
    coingecko_list = cg.get_coins()
    for i in coingecko_list:
        if(i['symbol'] == coin):
            id = i['id']
    price_coin_usd = float(cg.get_price(id,'usd')[id]['usd'])*float(number)

    return price_coin_usd

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

@bot.message_handler(content_types=['text'])
def coins(message):
    all_coins = coins_list()
    all_geckocoins = coingecko_list()
    splitmessage = message.text.split()
    if(len(splitmessage)>1 and len(splitmessage)<3):
        if((isfloat(splitmessage[0]))==True) and (float(splitmessage[0]) <  bignumber):
            if str((splitmessage[1])).upper() in all_coins and str((splitmessage[1]).lower()) in all_geckocoins:
                priceinminter = get_balance_full(float(splitmessage[0]),str(splitmessage[1]).upper())
                priceingecho = gecho_calc(float(splitmessage[0]),str(splitmessage[1]).lower())
                textminter = str(splitmessage[0])+" "+str(splitmessage[1]).upper()+ ": \n🍪 " + str(priceinminter[0]) + " BIP\n💰 " + str(place_value(round(priceinminter[1],6))) + " $\n"
                textgecho = "🦎 " + str(place_value(round(priceingecho,4))) + " $"
                alltext = textminter + textgecho
                bot.send_message(chat_id=message.chat.id,text=alltext)

            elif str((splitmessage[1])).upper() in all_coins:
                if(str((splitmessage[1])).upper()=='BIP'):
                    bip_price = round(float(cg.get_price(ids='bip', vs_currencies='usd')['bip']['usd'])*float(splitmessage[0]),4)
                    cost = get_bithump_price();
                    price = round(float(splitmessage[0]) * float(cost['c']),4)
                    textminter = str(splitmessage[0])+" "+str(splitmessage[1]).upper()+ ": \n🍪 "+str(place_value(price)) + " $\n🦎 "+ str(place_value(bip_price)) + " $"

                    text = textminter


                    bot.send_message(chat_id=message.chat.id,text=text,parse_mode="html")

                elif(str(splitmessage[1]).upper()=='BIT'):
                    balance_bit = get_balance_bit_full(float(splitmessage[0]));
                    text = str(splitmessage[0])+" "+str(splitmessage[1]).upper()+ ": \n🍪 " + str(place_value(round(balance_bit,4))) + " BIP"
                    bot.send_message(chat_id=message.chat.id,text=text)

                else:
                    priceofnumber = get_balance_full(float(splitmessage[0]),str(splitmessage[1]).upper())
                    if (priceofnumber[0] == 'error'):
                        text = '💬 Количество выпущенных монет менее запрашиваемой суммы'
                        bot.send_message(chat_id=message.chat.id,text=text)

                    else:
                        text = str(splitmessage[0])+" "+str(splitmessage[1]).upper()+ ": \n🍪 " + str(place_value(priceofnumber[0])) + " BIP\n💰 " + str(place_value(round(priceofnumber[1],4))) + " $"
                        bot.send_message(chat_id=message.chat.id,text=text)
            else:
                if str((splitmessage[1])).lower() in all_geckocoins:
                    priceofnumber = gecho_calc(float(splitmessage[0]),str(splitmessage[1]).lower())
                    text = str(splitmessage[0])+" "+str(splitmessage[1]).upper()+ ": \n💰 " + str(place_value(round(priceofnumber,4))) + " $"
                    bot.send_message(chat_id=message.chat.id,text=text)

    else:
        if message.text.upper() in all_coins and message.text.lower() in all_geckocoins:
            course = get_balance(message.text.upper())
            price_coin_usd = str(get_gecho_balance(message.text.lower()))
            textminter = "1 "+message.text.upper() + ": \n🍪 " + str(place_value(round(course[0],4))) + " BIP\n💰 " + str(place_value(round(course[1],6))) + " $\n"
            textgecho = "🦎 " + price_coin_usd + " $"
            alltext = textminter + textgecho
            bot.send_message(chat_id=message.chat.id,text=alltext)

        elif message.text.upper() in all_coins:
            if (message.text.upper() == 'BIP'):
                bip_price = round(float(cg.get_price(ids='bip', vs_currencies='usd')['bip']['usd']),6)
                cost = get_bithump_price();
                price = round((float(cost['c'])),6)
                text = "1 "+message.text.upper() + ": \n🍪 "+ str(place_value(price)) + " $\n🦎 " + str(place_value(round(bip_price,6))) + " $"
                bot.send_message(chat_id=message.chat.id,text=text)

            elif (message.text.upper() == 'BIT'):
                balance_bit = get_balance_bit()
                text = "1 "+message.text.upper() + ": \n🍪 " + str(place_value(round(balance_bit,4))) + " BIP"
                bot.send_message(chat_id=message.chat.id,text=text)


            else:
                course = get_balance(message.text.upper())
                if(course[0] == 'error'):
                    text = '💬 Количество выпущенных монет менее запрашиваемой суммы'
                    bot.send_message(chat_id=message.chat.id,text=text)
                else:
                    text = "1 "+message.text.upper() + ": \n🍪 " + str(place_value(course[0])) + " BIP\n💰 " + str(place_value(round(course[1],4))) + " $"
                    bot.send_message(chat_id=message.chat.id,text=text)

        else:
            if message.text.lower() in all_geckocoins:
                price_coin_usd = place_value(get_gecho_balance(message.text.lower()))
                text = "1 " + message.text.upper() + ": \n💰 " + str(price_coin_usd) + " $"
                bot.send_message(chat_id=message.chat.id,text=text)

bot.polling(none_stop=True, interval=0)
