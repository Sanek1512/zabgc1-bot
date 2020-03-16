# -*- coding: utf-8 -*-
import parserq
import data_processing

import threading
import time
import datetime

import telebot
from telebot import types
from telebot.types import Message
#   <-- Telegramm бот -->

token = open('TOKEN')
bot = telebot.TeleBot(token.read())

# Таблица, содержащая данные с сайта
table = []

# Нужно ли запрашивать новые данные с сайта?
delay = False

# дополнительная клавиатура
keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Все расписания занятий','Новые замены')

# Задержка (чтобы не DDOS'ить сервер сайта, а отпралять уже добытую таблицу)
def thread_delay():
    global delay
    # ЗАДЕРЖКА есть
    delay = True
    time.sleep(300)
    #ЗАДЕРЖКИ нет
    delay = False

def SetInformationTable():
    global table
    html_array = parserq.Parse()
    table = data_processing.GetTable(html_array)

# Вывод всех расписаний
def GetAllInformationTable(message):
    msg = ''
    for i in table:
        msg = str.format(i[0] + "\nСкачать: " + i[1] + "\n\nСмотреть: " + i[2])
        bot.send_message(message.chat.id, msg, reply_markup = keyboard1)

# Вывод сегодняшней и новых замен
def GetNewReplacements(message):
    msg = ''
    now_day = datetime.datetime.now().day
    
    for i in table:
        label = i[0]
        l_index = str(label).find(" на")
        dot = str(label).find(".")

        label_date = label[l_index+4:dot]

        try:
            d = int(label_date)
        except ValueError:
            continue

        if d >= now_day:
            msg = str.format(label + "\nСкачать: " + i[1] + "\n\nСмотреть: " + i[2])
            bot.send_message(message.chat.id, msg, reply_markup = keyboard1)

# реагировать на команды 
@bot.message_handler(commands=['start'])
def command_handler(message: Message):
    start_message = str.format(
    "👋 Привет, "+ str(message.from_user.first_name) + " " + str(message.from_user.last_name) +
    "\nЯ - программа-бот, и с моей помощью Вы можете посмотреть замены в расписании не заходя на сайт.\n\n" +
    "Чтобы узнать замены на сегодня и завтра нажми кнопку 'Новые замены'\n\n" +
    "📩 Вопросы и предложения присылайте сюда: " +
    "https://vk.com/ti10x\n\n" +
    "💡 Взгляните на расписание в виде картинок: " +
    "https://drive.google.com/drive/folders/18m1Ir1yH4mFSuNrfTO9b1AoSc2YnYipM"
    )
    bot.send_message(message.chat.id, start_message, reply_markup=keyboard1)

# реагировать на чатовые сообщения
@bot.message_handler(content_types=['text'])
def send_text(message):
    global delay

    if delay == False:
        if message.text.lower() == 'все расписания занятий':
            SetInformationTable()
            GetAllInformationTable(message)

        if message.text.lower() == 'новые замены':
            SetInformationTable()
            GetNewReplacements(message)

        x = threading.Thread(target=thread_delay, daemon=False)
        x.start()
    else:
        if message.text.lower() == 'все расписания занятий':
            GetAllInformationTable(message)
        if message.text.lower() == 'новые замены':
            GetNewReplacements(message)

# Всегда проверять что написал пользователь
bot.polling(none_stop=True, interval=0)
