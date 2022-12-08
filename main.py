import telebot
import random
from telebot import types
bot = telebot.TeleBot('5981604358:AAHCMTf7_Kt5GSIJjI3NGCVK5ecsXhHoz2E')

FILE1 = r'easy.txt'
FILE2 = r'moderate.txt'
FILE3 = r'hard.txt'
FILE4 = r'english.txt'

users = {}
commands_score = {}
players = {}
commands_counter = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Начать игру')
    button_follow_invitation = types.KeyboardButton('Присоединиться к игре')
    button_rules = types.KeyboardButton('Прочитать правила')
    markup.row(button_start)
    markup.row(button_rules)
    markup.row(button_follow_invitation)
    bot.send_message(message.from_user.id, 'Добро пожаловать в бота для игры в Шляпу (Alias)', reply_markup=markup)
    bot.register_next_step_handler(message, play_or_read)

def play_or_read(message):
    if message.text == 'Начать игру':
        get_command_amount(message)
    elif message.text == 'Присоединиться к игре':
        enter_guest(message)
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

def enter_guest(message):
    bot.send_message(message.from_user.id, 'Введите код игры, к которой хотите присоединиться')
    bot.register_next_step_handler(message, check_guest)

def check_guest(message):
    try:
        if int(message.text) in players.keys():               # players {321654564654: [12345678, 12345679, 12345677]    }
            players[message.text].append(message.chat.id)
            bot.send_message(message.from_user.id, 'Вы успешно присоединились к игре')
        else:
            bot.send_message(message.from_user.id, 'Введён неверный код. Такой игры нет. Попробуйте ещё раз.')
            enter_guest(message)
    except ValueError:
        bot.send_message(message.from_user.id,
                         'Введён неверный код. Код должен состоять только из цифр. Попробуйте ещё раз.')
        enter_guest(message)


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
                bot.register_next_step_handler(message, victory_score)
            else:
                for i in users[chat_id]['command_name']:
                    commands_score[i] = 0
                bot.register_next_step_handler(message, victory_score)
    else:
        bot.send_message(message.from_user.id, 'Ваш ответ не распознан, нажми на кнопку')
        bot.register_next_step_handler(message, command_name)

def victory_score(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button25 = types.KeyboardButton('25')
    button50 = types.KeyboardButton('50')
    button100 = types.KeyboardButton('100')
    keyboard.row(button25, button50, button100)
    bot.send_message(message.from_user.id, 'До скольки очков играем для победы?', reply_markup=keyboard)
    bot.register_next_step_handler(message, set_victory_score)

def set_victory_score(message):
    chat_id = message.chat.id
    if message.text in ['25', '50', '100']:
        users[chat_id]['score'] = int(message.text)
        penalty(message)
    else:
        bot.send_message(message.from_user.id, 'Ваш ответ не распознан, нажми на кнопку')
        victory_score(message)

def penalty(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_yes = types.KeyboardButton('Да')
    button_no = types.KeyboardButton('Нет')
    keyboard.row(button_yes, button_no)
    bot.send_message(message.from_user.id, 'Отнимать ли очки за пропуск хода?', reply_markup=keyboard)
    bot.register_next_step_handler(message, set_penalty)

def set_penalty(message):
    chat_id = message.chat.id
    if message.text.lower() == 'да':
        users[chat_id]['penalty'] = True
        explain_time(message)
    elif message.text.lower() == 'нет':
        users[chat_id]['penalty'] = False
        explain_time(message)

def explain_time(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_60 = types.KeyboardButton('60')
    button_90 = types.KeyboardButton('90')
    button_120 = types.KeyboardButton('120')
    keyboard.row(button_60, button_90, button_120)
    bot.send_message(message.from_user.id, 'Сколько времени даём на объяснение?', reply_markup=keyboard)
    bot.register_next_step_handler(message, set_explain_time)

def set_explain_time(message):
    chat_id = message.chat.id
    if message.text.lower() == '60':
        users[chat_id]['explain_time'] = int(message.text)
        choose_dict(message)
    elif message.text.lower() == '90':
        users[chat_id]['explain_time'] = int(message.text)
        choose_dict(message)
    elif message.text.lower() == '120':
        users[chat_id]['explain_time'] = int(message.text)
        choose_dict(message)

def choose_dict(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_easy = types.KeyboardButton('Простой')
    button_moderate = types.KeyboardButton('Средний')
    button_hard = types.KeyboardButton('Сложный')
    button_english = types.KeyboardButton('Английский')
    keyboard.row(button_easy, button_moderate, button_hard, button_english)
    bot.send_message(message.from_user.id, 'Выбери словарь для игры', reply_markup=keyboard)
    bot.register_next_step_handler(message, create_dict)

def create_dict(message):
    chat_id = message.chat.id
    if message.text.lower() == 'простой':
        with open(FILE1, encoding='utf-8') as f:
            easy = f.readlines()
            easy = [line.rstrip('\n') for line in easy]
            users[chat_id]['dictionary'] = easy
            random.shuffle(users[chat_id]['dictionary'])
            create_game_code(message)
            #return users
    elif message.text.lower() == 'средний':
        with open(FILE2, encoding='utf-8') as f:
            moderate = f.readlines()
            moderate = [line.rstrip('\n') for line in moderate]
            users[chat_id]['dictionary'] = moderate
            random.shuffle(users[chat_id]['dictionary'])
            create_game_code(message)
            #return users
    elif message.text.lower() == 'сложный':
        with open(FILE3, encoding='utf-8') as f:
            hard = f.readlines()
            hard = [line.rstrip('\n') for line in hard]
            users[chat_id]['dictionary'] = hard
            random.shuffle(users[chat_id]['dictionary'])
            create_game_code(message)
            #return users
    elif message.text.lower() == 'английский':
        with open(FILE4, encoding='utf-8') as f:
            english = f.readlines()
            english = [line.rstrip('\n') for line in english]
            users[chat_id]['dictionary'] = english
            random.shuffle(users[chat_id]['dictionary'])
            create_game_code(message)
            #return users
    print(users)


def create_game_code(message):
    code = random.randint(10000000, 999999999999)
    players[code] = [message.chat.id]
    bot.send_message(message.from_user.id, f'Ваш код: {code}')
    start_circle(message)

def start_circle(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Начать объяснение!')
    keyboard.row(button_start)
    active_command = users[chat_id]['command_name'][commands_counter]
    bot.send_message(message.from_user.id,
                       f"Объясняет команда {active_command}", reply_markup=keyboard)
    echo(message, f"Объясняет команда {active_command}")


def echo(message, text):
    chat_id = message.chat.id
    for i in players.values():
        if message.chat_id in i:
            i.remove(chat_id)
            for j in i:
                bot.send_message(j, text)
            break

#def set_players(message):
#    if not players.get(message.chat.id):
#        code = random.randint(10000000, 999999999999)
#        players[code] = [message.chat.id]
#        bot.send_message(message.from_user.id, f'Ваш код: {code}')
#
#    if int(message.text) in players.keys():               # players {321654564654: [12345678, 12345679, 12345677]    }
#        for i in players[message.text]:
#            bot.send_message(i, 'Добавлен новый участник!')
#        players[message.text].append(message.chat.id)
#    for i in User.users:
#        if not User.users[i]:
#            User.users[i] = int(message.chat.id)
#            User.users[message.chat.id] = i
#            bot.send_message(message.from_user.id, 'Собеседник найден, можете начинать диалог!')
#            bot.send_message(i, 'Собеседник найден, можете начинать диалог!')





if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()