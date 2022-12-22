import random

counters = {'not_change_counter_true': 0, 'not_change_counter_false': 0,
            'change_counter_true': 0, 'change_counter_false': 0}

def play1():

    for i in range (0, 1000000):
        doors = ['True', 'False', 'False']
        random.shuffle(doors)
        choice = random.randint(0, 2)
        if doors[choice] == 'True':
            counters['not_change_counter_true'] += 1
        else:
            counters['not_change_counter_false'] += 1

def play2():
    for i in range (0, 1000000):
        doors = ['True', 'False', 'False']
        random.shuffle(doors)
        my_choice = random.randint(0, 2)
        if my_choice == 0 and doors[0] == 'True':
            counters['change_counter_false'] += 1
        elif my_choice == 0 and doors[1] == 'True':
            counters['change_counter_true'] += 1
        elif my_choice == 0 and doors[2] == 'True':
            counters['change_counter_true'] += 1
        elif my_choice == 1 and doors[0] == 'True':
            counters['change_counter_true'] += 1
        elif my_choice == 1 and doors[1] == 'True':
            counters['change_counter_false'] += 1
        elif my_choice == 1 and doors[2] == 'True':
            counters['change_counter_true'] += 1
        elif my_choice == 2 and doors[0] == 'True':
            counters['change_counter_true'] += 1
        elif my_choice == 2 and doors[1] == 'True':
            counters['change_counter_true'] += 1
        elif my_choice == 2 and doors[2] == 'True':
            counters['change_counter_false'] += 1

if __name__ == '__main__':
    play1()
    play2()
    print(counters)