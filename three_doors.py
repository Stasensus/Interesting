"""
Данный скрипт доказывает интересную задачу из теории вероятности. Перед вами три двери, вам известно, что за одной из них
приз. Вы выбираете одну дверь. Но ведущий открывает вам другую дверь, за которой пусто, и предлагает поменять своё решение
- из оставшихся двух дверей выбрать другую, чтобы найти приз. Целесообразно ли менять своё решение? Могут ли ваши шансы
вырасти?
"""
import random

counters = {'Не поменял и угадал': 0, 'Не поменял и не угадал': 0, #счётчик угадываний, если решение НЕ меняется
            'Поменял и угадал': 0, 'Поменял и не угадал': 0} #счётчик угадываний, если решение МЕНЯЕТСЯ

def play_not_change_choice():

    for i in range (0, 1000000):
        doors = ['True', 'False', 'False']
        random.shuffle(doors)
        choice = random.randint(0, 2)
        if doors[choice] == 'True':
            counters['Не поменял и угадал'] += 1
        else:
            counters['Не поменял и не угадал'] += 1

def play_change_choice():
    for i in range (0, 1000000):
        doors = ['True', 'False', 'False']
        random.shuffle(doors)
        my_choice = random.randint(0, 2)
        if my_choice == 0 and doors[0] == 'True':
            counters['Поменял и не угадал'] += 1
        elif my_choice == 0 and doors[1] == 'True':
            counters['Поменял и угадал'] += 1
        elif my_choice == 0 and doors[2] == 'True':
            counters['Поменял и угадал'] += 1
        elif my_choice == 1 and doors[0] == 'True':
            counters['Поменял и угадал'] += 1
        elif my_choice == 1 and doors[1] == 'True':
            counters['Поменял и не угадал'] += 1
        elif my_choice == 1 and doors[2] == 'True':
            counters['Поменял и угадал'] += 1
        elif my_choice == 2 and doors[0] == 'True':
            counters['Поменял и угадал'] += 1
        elif my_choice == 2 and doors[1] == 'True':
            counters['Поменял и угадал'] += 1
        elif my_choice == 2 and doors[2] == 'True':
            counters['Поменял и не угадал'] += 1

if __name__ == '__main__':
    play_not_change_choice()
    play_change_choice()
    print(counters)

