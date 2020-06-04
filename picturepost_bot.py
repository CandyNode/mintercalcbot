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

API_TOKEN = '1153028894:AAH3eHGE2jBexP61nG-HBiHGkBug2lvUzeI'
bot = telebot.TeleBot(API_TOKEN)
cwd = os.getcwd()
cg = CoinGeckoAPI()
bignumber = 10000000001

#@bot.message_handler(commands=['start', 'help'])
#@bot.message_handler(func=lambda message: message.text == 'Привет')
#def send_welcome(message):

    #bot.send_message(message.chat.id,text='Привет всем!\n\nЯ простой бот, может я не такой способный, как мои собратья, но я умею главное - держать Вас в курсе последней цены.\n\nА еще я нарисовал для вас картинку...\nОна не совсем простая, когда с нашим BIP все хорошо, она зеленеет, а когда становится хуже, я краснею от злости и делаю ее красной, пользуйтесь на здоровье!\n\nДля получения цены введите команду /biphumb')

def get_bithump_price():

    URL_BIP_COST_BITHUMP='https://global-openapi.bithumb.pro/market/data/ticker?symbol=BIP-USDT'
    bithump_url=requests.get(URL_BIP_COST_BITHUMP)
    sell_usdt=[]
    buy_usdt=[]
    data = bithump_url.json()['info'][0]

    return(data)

@bot.message_handler(commands=['biphumb', 'bithumb'])
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

bot.polling(none_stop=True, interval=0)
