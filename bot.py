import telebot
import sqlite3
from telebot.types import ReplyKeyboardMarkup
from telebot import types
import db_client

bot = telebot.TeleBot('6169079001:AAHapI0BGHHzAGeTjujFHqETKttjVElCVgY')

con = sqlite3.connect('sqlite.db')
cur = con.cursor()

cur.execute('CREATE TABLE IF NOT EXISTS chat_room ('
            'id INTEGER primary key AUTOINCREMENT,'
            'chat_id1 varchar,'
            'chat_id2 varchar,'
            'status varchar)')



print(1)
con.commit()
chat_id = ''

@bot.message_handler()
def start(message):
    global chat_id
    if message.text == '/start':
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row('Начать общаться')
        bot.send_message(message.chat.id,
                         'Привет, это бот для '
                         'анонимного общения', reply_markup=menu)
    elif message.text == 'Начать общаться':
        chat_rooms = db_client.search_free_chat_rooms()
        if len(chat_rooms) == 0:
            db_client.create_chat_room(message.chat.id)
            bot.send_message(message.chat.id, 'Ожидание собеседника')
        else:
            db_client.start_chat_room(chat_rooms[0][0], message.chat.id)
            menu = ReplyKeyboardMarkup(resize_keyboard=True)
            menu.row('Завершить диалог', 'Отправить телефон')
            bot.send_message(chat_rooms[0][1], 'Ваш собеседник найден', reply_markup=menu)
            bot.send_message(message.chat.id, 'Ваш собеседник найден', reply_markup=menu)
    elif message.text == 'Завершить диалог':
        chat = db_client.end_chat(message.chat.id)
        menu = ReplyKeyboardMarkup(resize_keyboard=True)
        menu.row('Начать общаться')
        bot.send_message(message.chat.id, 'Ваш диалог был прекращен')
        bot.send_message(chat, 'Ваш диалог был прекращен', reply_markup=menu)
        chat_id = ''
    elif message.text == 'Отправить телефон':
        bot.send_message(chat_id, f'@{message.from_user.username}')
        print(1)
    else:
        if chat_id == '' or chat_id == str(message.chat.id):
            c = db_client.search_current_chat_room(message.chat.id)
            if c[0][1] != str(message.chat.id):
                chat_id = c[0][1]
            else:
                chat_id = c[0][2]
        print(chat_id)
        bot.send_message(chat_id, message.text)

bot.polling()