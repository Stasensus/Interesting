import time
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
temp_words_list = []


class Time:
    def time_start(self, message):
        chat_id = message.chat.id
        #users[chat_id] = {'time_starts': time.perf_counter()}
        #self.time_starts = time.perf_counter()
        users[chat_id]['start time'] = time.perf_counter()

    def time_check(self, message):
        chat_id = message.chat.id
        #self.time_current = time.perf_counter()
        users[chat_id]['current time'] = time.perf_counter()
        #if self.time_current - self.time_starts < users[chat_id]['explain_time']:
        if users[chat_id]['current time'] - users[chat_id]['start time'] < users[chat_id]['explain_time']:
            return True
        else:
            return False


Object_time = Time()


class Counters:
    commands_counter = 0
    temporary_score_counter = 0
    words_counter = 0


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Начать игру')
    button_follow_invitation = types.KeyboardButton('Присоединиться к игре')
    button_rules = types.KeyboardButton('Прочитать правила')
    markup.row(button_start)
    markup.row(button_rules)
    markup.row(button_follow_invitation)
    bot.send_message(message.chat.id, 'Добро пожаловать в бота для игры в Шляпу (Alias)', reply_markup=markup)
    bot.register_next_step_handler(message, play_or_read)


def play_or_read(message):
    if message.text == 'Начать игру':
        get_command_amount(message)
    elif message.text == 'Присоединиться к игре':
        enter_guest(message)
    elif message.text == 'Прочитать правила':
        show_rules(message)
    else:
        bot.send_message(message.chat.id, 'Напиши /start')


def show_rules(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_back = types.KeyboardButton('Начать игру')
    markup.row(button_back)
    bot.send_message(message.chat.id, 'Правила игры таковы: ... ', reply_markup=markup)
    bot.register_next_step_handler(message, get_command_amount)


def enter_guest(message):
    bot.send_message(message.chat.id, 'Введите код игры, к которой хотите присоединиться')
    bot.register_next_step_handler(message, check_guest)


def check_guest(message):
    try:
        if int(message.text) in players.keys():

            players[int(message.text)].append(message.chat.id)

            bot.send_message(message.chat.id, 'Вы успешно присоединились к игре')
        else:
            bot.send_message(message.chat.id, 'Введён неверный код. Такой игры нет. Попробуйте ещё раз.')
            enter_guest(message)
    except ValueError:
        bot.send_message(message.chat.id,
                         'Введён неверный код. Код должен состоять только из цифр. Попробуйте ещё раз.')
        enter_guest(message)


def get_command_amount(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button2 = types.KeyboardButton('2')
    button3 = types.KeyboardButton('3')
    button4 = types.KeyboardButton('4')
    button5 = types.KeyboardButton('5')
    markup.row(button2, button3, button4, button5)
    bot.send_message(message.chat.id, 'Сколько команд будет играть?', reply_markup=markup)
    bot.register_next_step_handler(message, set_command_amount)


def set_command_amount(message):
    chat_id = message.chat.id
    users[chat_id] = {
        'command_amount': int(message.text),
        'command_name': [],
    }
    bot.send_message(message.chat.id, 'Введите название команды №1:')
    bot.register_next_step_handler(message, command_name)


def command_name(message):
    chat_id = message.chat.id
    if users.get(chat_id):
        if len(users.get(chat_id)['command_name']) != users.get(chat_id)['command_amount']:
            users[chat_id]['command_name'].append(message.text)
            if len(users.get(chat_id)['command_name']) + 1 <= users.get(chat_id)['command_amount']:
                bot.send_message(message.chat.id,
                                 f"Введите название команды №{len(users.get(chat_id)['command_name']) + 1}: ")
                bot.register_next_step_handler(message, command_name)
            else:
                for i in users[chat_id]['command_name']:
                    commands_score[i] = 0
                print(commands_score)
                victory_score(message)
    else:
        bot.send_message(message.chat.id, 'Ваш ответ не распознан, нажми на кнопку')
        bot.register_next_step_handler(message, command_name)


def victory_score(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button25 = types.KeyboardButton('10')
    button50 = types.KeyboardButton('50')
    button100 = types.KeyboardButton('100')
    keyboard.row(button25, button50, button100)
    bot.send_message(message.chat.id, 'До скольки очков играем для победы?', reply_markup=keyboard)
    bot.register_next_step_handler(message, set_victory_score)


def set_victory_score(message):
    chat_id = message.chat.id
    if message.text in ['10', '50', '100']:
        users[chat_id]['score'] = int(message.text)
        penalty(message)
    else:
        bot.send_message(message.chat.id, 'Ваш ответ не распознан, нажми на кнопку')
        victory_score(message)


def penalty(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_yes = types.KeyboardButton('Да')
    button_no = types.KeyboardButton('Нет')
    keyboard.row(button_yes, button_no)
    bot.send_message(message.chat.id, 'Отнимать ли очки за пропуск хода?', reply_markup=keyboard)
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
    button_60 = types.KeyboardButton('15')
    button_90 = types.KeyboardButton('90')
    button_120 = types.KeyboardButton('120')
    keyboard.row(button_60, button_90, button_120)
    bot.send_message(message.chat.id, 'Сколько времени даём на объяснение?', reply_markup=keyboard)
    bot.register_next_step_handler(message, set_explain_time)


def set_explain_time(message):
    chat_id = message.chat.id
    if message.text.lower() == '15':
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
    bot.send_message(message.chat.id, 'Выбери словарь для игры', reply_markup=keyboard)
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
            # return users
    elif message.text.lower() == 'средний':
        with open(FILE2, encoding='utf-8') as f:
            moderate = f.readlines()
            moderate = [line.rstrip('\n') for line in moderate]
            users[chat_id]['dictionary'] = moderate
            random.shuffle(users[chat_id]['dictionary'])
            create_game_code(message)
            # return users
    elif message.text.lower() == 'сложный':
        with open(FILE3, encoding='utf-8') as f:
            hard = f.readlines()
            hard = [line.rstrip('\n') for line in hard]
            users[chat_id]['dictionary'] = hard
            random.shuffle(users[chat_id]['dictionary'])
            create_game_code(message)
            # return users
    elif message.text.lower() == 'английский':
        with open(FILE4, encoding='utf-8') as f:
            english = f.readlines()
            english = [line.rstrip('\n') for line in english]
            users[chat_id]['dictionary'] = english
            random.shuffle(users[chat_id]['dictionary'])
            create_game_code(message)
            # return users
    print(users)


def create_game_code(message):
    code = random.randint(10000000, 999999999999)
    players[code] = [message.chat.id]
    bot.send_message(message.chat.id, f'Ваш код: {code}')
    start_circle(message)


def echo(message, text):
    chat_id = message.chat.id
    for i in players.values():
        if message.chat.id in i:
            for j in i:
                if j != chat_id:
                    bot.send_message(j, text)
            break


def start_circle(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Начать объяснение!')
    keyboard.row(button_start)
    active_command = users[chat_id]['command_name'][Counters.commands_counter]
    bot.send_message(message.chat.id,
                     f"Объясняет команда {active_command}", reply_markup=keyboard)
    echo(message, f"Объясняет команда {active_command}")
    bot.register_next_step_handler(message, start_explanation)


def start_explanation(message):
    Counters.temporary_score_counter = 0
    Object_time.time_start(message)
    # temp_words_list = []    Не забыть обнулить каждый ход!
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_next = types.KeyboardButton('Следующее слово')
    button_skip = types.KeyboardButton('Пропустить слово')
    keyboard.row(button_next, button_skip)
    bot.send_message(message.chat.id,
                     users[chat_id]['dictionary'][Counters.words_counter], reply_markup=keyboard)
    echo(message, {users[chat_id]['dictionary'][Counters.words_counter]})
    bot.register_next_step_handler(message, demonstrate_word)


def demonstrate_word(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_next = types.KeyboardButton('Следующее слово')
    button_skip = types.KeyboardButton('Пропустить слово')
    keyboard.row(button_next, button_skip)
    count_words()
    if message.text.lower() == 'следующее слово':
        Counters.temporary_score_counter += 1
        temp_words_list.append(users[chat_id]['dictionary'][Counters.words_counter])
        print(temp_words_list)

    elif message.text.lower() == 'пропустить слово':
        if users[chat_id]['penalty'] == True:
            Counters.temporary_score_counter -= 1
            if Counters.temporary_score_counter < 0:
                Counters.temporary_score_counter = 0

    if Object_time.time_check(message) == True:
        bot.send_message(message.chat.id,
                         users[chat_id]['dictionary'][Counters.words_counter], reply_markup=keyboard)
        echo(message, users[chat_id]['dictionary'][Counters.words_counter])
        bot.register_next_step_handler(message, demonstrate_word)
    else:
        bot.send_message(message.chat.id,
                         'Время истекло!')
        echo(message, 'Время истекло!')
        finish_explanation(message)


def finish_explanation(message):
    bot.send_message(message.chat.id,
                     'Были объяснены слова:')
    echo(message, 'Были объяснены слова:')
    bot.send_message(message.chat.id,
                     '\n'.join(temp_words_list))
    echo(message, '\n'.join(temp_words_list))
    bot.send_message(message.chat.id,
                     'Сколько слов объяснено неправильно? Напишите цифру. Если все правильно, введите "0"')
    echo(message, 'Сколько слов объяснено неправильно? Напишите цифру. Если все правильно, введите "0"')
    bot.register_next_step_handler(message, finish_explanation_2)


def finish_explanation_2(message):
    if message.text.isdigit():
        Counters.temporary_score_counter -= int(message.text)
        finish_explanation_3(message)
    else:
        bot.send_message(message.chat.id, 'Вы ввели не число. Введите число')
        bot.register_next_step_handler(message, finish_explanation_2)



def finish_explanation_3(message):
    chat_id = message.chat.id
    print(commands_score)
    if Counters.temporary_score_counter < 0:
        Counters.temporary_score_counter = 0
    active_command = users[chat_id]['command_name'][Counters.commands_counter]
    commands_score[active_command] += Counters.temporary_score_counter
    bot.send_message(message.chat.id,
                     f'Ваша команда набрала {Counters.temporary_score_counter} очков')
    echo(message, f'Ваша команда набрала {Counters.temporary_score_counter} очков')
    finish_explanation_4(message)

def finish_explanation_4(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_start = types.KeyboardButton('Начать объяснение!')
    keyboard.row(button_start)
    if Counters.commands_counter + 1 < users.get(chat_id)['command_amount']:
        Counters.commands_counter += 1
        active_command = users[chat_id]['command_name'][Counters.commands_counter]
        bot.send_message(message.chat.id,
                         f"Объясняет команда {active_command}", reply_markup=keyboard)
        echo(message, f"Объясняет команда {active_command}")
        start_explanation(message)
    else:
        finish_circle(message)


def finish_circle(message):
    chat_id = message.chat.id
    for i in commands_score:
        bot.send_message(message.chat.id,
                         f'Команда {i} набрала {commands_score[i]} очков')
        echo(message, f'Команда {i} набрала {commands_score[i]} очков')
    for i in users[chat_id]['command_name']:
        if commands_score[i] >= users[chat_id]['score']:
            congratulate(message)
            break
    else:
        Counters.commands_counter = 0
        start_circle(message)


def congratulate(message):
    chat_id = message.chat.id
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_one_more = types.KeyboardButton('Сыграть ещё раз')
    keyboard.row(button_one_more)
    bot.send_message(message.chat.id,
                     'Игра окончена!')
    echo(message, 'Игра окончена!')
    for i in commands_score:
        if commands_score[i] == max(commands_score.values()):
            bot.send_message(message.chat.id,
                             f'Победила команда {i}', reply_markup=keyboard)
            echo(message, f'Победила команда {i}')


"""
Функция ниже нигде не используется
"""


# def zero_counter(self, event):
#     user_id = event.user_id
#     if not self.bot.users[user_id].get('words counter'):
#         self.bot.users[user_id]['words counter'] = 0
#     return self.bot.users[user_id]['words counter']

def count_words():
    Counters.words_counter += 1
    return Counters.words_counter


def score_counter(self, command_title):
    self.bot.commands_score[command_title] += 1


def commands_count(self, event):
    user_id = event.user_id
    self.commands_counter += 1
    if self.commands_counter >= self.bot.users.get(user_id)['command_amount']:
        self.commands_counter = 0


def set_temp_counter_2zero(self):
    self.__temp_counter = 0


def temp_score_counter(self):
    self.__temp_counter += 1


# def finish_explaination(self, event):
#     user_id = event.user_id
#     self.bot._send_msg(user_id, "Время истекло!")
#     print(self.bot.commands_score)
#     self.commands_count(event)
#     self.game_starter(event)


if __name__ == '__main__':
    print("Бот запущен!")
    bot.infinity_polling()
