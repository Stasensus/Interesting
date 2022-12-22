import random

counters = {'first_time_counter': 0, 'change_counter_true': 0, 'not_change_counter_true': 0,
                'change_counter_false': 0, 'not_change_counter_false': 0}


def play():
    doors = ['True', 'False', 'False']
    doors2 = [1, 2, 3]
    random.shuffle(doors)
    dilemma = 'change'
    print(dilemma)
    print(counters)
    # if doors[0] == 'True':
    #     x = random.randint(1, 2)
    #     y = 3 - x
    #     doors2[0] = '?'
    #     doors2[x] = 'False'
    #     doors2[y] = '?'
    # elif doors[1] == 'True':
    #     x = 2*(random.randint(0, 1))
    #     y = 2 - x
    #     doors2[1] = '?'
    #     doors2[x] = 'False'
    #     doors2[y] = '?'
    # else:
    #     x = random.randint(0, 1)
    #     y = 1 - x
    #     doors2[2] = '?'
    #     doors2[x] = 'False'
    #     doors2[y] = '?'
    #print(doors2)
    my_choice = random.randint(0, 2)
    if doors[my_choice] == 'True':
        counters['first_time_counter'] += 1

        play()

    else:
        if dilemma == 'change':
            if my_choice == 0 and doors[2] == 'True':
                my_choice = 2
            elif my_choice == 0 and doors[1] == 'True':
                my_choice = 1
            elif my_choice == 1 and doors[0] == 'True':
                doors2 = ['???', '???', 'False']
            elif my_choice == 1 and doors[2] == 'True':
                doors2 = ['False', '???', '???']
            elif my_choice == 2 and doors[0] == 'True':
                doors2 = ['???', 'False', '???']
            elif my_choice == 2 and doors[1] == 'True':
                doors2 = ['False', '???', '???']

            my_choice = int(input('Какую дверь ты выбираешь?'))
            my_choice -= 1
            if doors[my_choice] == 'True':
                print(doors)
                print('Ты поменял решение и угадал!')
                counters['change_counter_true'] += 1
                play()
            elif doors[my_choice] == 'False':
                print(doors)
                print('Ты поменял решение и не угадал!')
                counters['change_counter_false'] += 1
                play()
        elif dilemma == 'N':
            if doors[my_choice] == 'True':
                print(doors)
                print('Ты упрямая барашка, не поменял решение и угадал!')
                counters['not_change_counter_true'] += 1
                play()
            elif doors2[my_choice] == 'False':
                print(doors)
                print('Ты упрямый баран, не поменял решение и не угадал!')
                counters['not_change_counter_false'] += 1
                play()


if __name__ == '__main__':


    play()

