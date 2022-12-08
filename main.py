import telebot
from telebot import types
bot = telebot.TeleBot('5981604358:AAHCMTf7_Kt5GSIJjI3NGCVK5ecsXhHoz2E')

users = {}
commands_score = {}

# @bot.message_handler(commands=['start'])
# def start(message):
#     #print(message.text)
#     #chat_id = message.chat.id
#     #bot.send_message(chat_id, 'Добро пожаловать в бота для игры в Шляпу (ALIAS):')
#     #bot.register_next_step_handler(message, get_name)
#     keyboard = types.InlineKeyboardMarkup()
#     a = types.InlineKeyboardButton('Начать игру', callback_data='Начать игру')
#     b = types.InlineKeyboardButton('Прочитать правила', callback_data='Прочитать правила')
#     keyboard.row(a, b)
#     bot.send_message(message.from_user.id, 'Добро пожаловать в бота для игры в Шляпу (Alias)', reply_markup=keyboard)
#     #if message.text == 'Начать игру':
#     #    bot.register_next_step_handler(message, get_command_amount)
#     #elif message.text == 'Прочитать правила':
#     #    bot.register_next_step_handler(message, show_rules)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Начать игру')
    button_rules = types.KeyboardButton('U+1F4D6 Прочитать правила')
    markup.row(button_start)
    markup.row(button_rules)
    bot.send_message(message.from_user.id, 'Добро пожаловать в бота для игры в Шляпу (Alias)', reply_markup=markup)
    bot.register_next_step_handler(message, play_or_read)


def play_or_read(message):
    if message.text == 'Начать игру':
        get_command_amount(message)
    elif message.text == 'Прочитать правила':
        show_rules(message)
    else:
        bot.send_message(message.from_user.id, 'Напиши /start')

def show_rules(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton('Начать игру')
    markup.row(button_back)
    bot.send_message(message.from_user.id, 'Правила игры таковы: ... ', reply_markup=markup)
    bot.register_next_step_handler(message, get_command_amount)

def get_command_amount(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('2')
    button3 = types.KeyboardButton('3')
    button4 = types.KeyboardButton('4')
    button5 = types.KeyboardButton('5')
    markup.row(button2, button3, button4, button5)
    bot.send_message(message.from_user.id, 'Сколько команд будет играть?', reply_markup=markup)
    bot.register_next_step_handler(message, set_command_amount)



def set_command_amount(message):
    chat_id = message.chat.id
    users[chat_id] = {
        'command_amount': int(message.text),
        'command_name': [],
    }
    bot.send_message(message.from_user.id, 'Введите название команды №1:')
    bot.register_next_step_handler(message, command_name)

def command_name(message):
    chat_id = message.chat.id
    if users.get(chat_id):
        if len(users.get(chat_id)['command_name']) != users.get(chat_id)['command_amount']:
            users[chat_id]['command_name'].append(message.text)
            if len(users.get(chat_id)['command_name']) + 1 <= users.get(chat_id)['command_amount']:
                bot.send_message(message.from_user.id,
                               f"Введите название команды №{len(users.get(chat_id)['command_name']) + 1}: ")
            else:
                for i in users[chat_id]['command_name']:
                    commands_score[i] = 0
                bot.register_next_step_handler(message, victory_score)
    else:
        bot.send_message(message.from_user.id, 'Ваш ответ не распознан')


def victory_score(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button25 = types.KeyboardButton('25')
    button50 = types.KeyboardButton('50')
    button100 = types.KeyboardButton('100')
    markup.row(button25, button50, button100)
    bot.send_message(message.from_user.id, 'До скольки очков играем для победы?', reply_markup=keyboard)
    bot.register_next_step_handler(message, set_victory_score)

def set_victory_score(message):





@bot.message_handler(content_types=['text'])
def abc(message):
    bot.send_message(message.from_user.id, 'Напиши /start')



if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()