import telebot
from telebot import types
import db_func as f

token = '594912100:AAHkEy-Ka3xWCCEmMSMFLCIqPHnhxaLaEjM'
bot = telebot.TeleBot(token)
f.setup()

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name)
        for name in
        ['/start_today', '/predict', '/statistic']]
        )

    if not f.check_user_in_bd():
        bot.send_message(message.chat.id, 'Начнем?',
            reply_markup=keyboard)
        f.add_user_to_bd

    else:
        bot.send_message(message.chat.id, 'Мы снова в главном меню',
            reply_markup=keyboard)


@bot.message_handler(commands=['start_today'])
def start_today(message):
    bot.send_message(
        message.chat.id, 'Я вас понял, я вас услышал'
    )
    f.write_to_db(message.chat.id)


@bot.message_handler(commands=['predict'])
def predict(message):
    period, next_date = get_period(), get_next_date()
    if period:
        bot.send_message(
            message.chat.id,
            'Примерно через {} дней, то есть {}'.format(period, next_date)
        )
    else:
        bot.send_message(
            message.chat.id,
            '''
            Недостаточно данных для предсказания.
            Внесите хотя бы одно значение в статистику.
            '''
            )


@bot.message_handler(commands=['statistic'])
def statistic(message):
    bot.send_message(
        message.chat.id,
        '''
        Извлекаем статистику...
        '''
        )
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        *[types.KeyboardButton(name)
        for name in
        ['/add_dates', '/show_data', '/go_back']]
        )
    bot.send_message(message.chat.id, 'Что будем делать?',
        reply_markup=keyboard)


@bot.message_handler(commands=['go_back'])
def go_back(message):
    start(message)


bot.polling()
