import json
import random
import math
import re

board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]


def read_data():
    with open('data.json', 'r') as f:
        return json.load(f)


def write_data(my_data):
    with open('data.json', 'w') as f:
        json.dump(my_data, f)


def random_choose(turn):
    while True:
        x = math.floor(random.random() * 3)
        y = math.floor(random.random() * 3)
        if board[x][y] == -1:
            board[x][y] = turn % 2
            return 'F' + str(x) + str(y)


def advance_choose(turn, action_log, my_data):
    print('first data size :', len(my_data), ' action :', action_log)
    n = len(action_log)
    if turn == 0 or turn == 1:
        return random_choose(turn)
    new_data = {}
    for i in my_data.keys():
        if len(i) >= n and i[:n] == action_log:
            new_data[i] = my_data[i]
    my_data = new_data
    print('access data :', new_data)
    if len(new_data) == 0:
        return random_choose(turn)
    step = []
    max_win = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] != -1:
                continue
            next_step = action_log + 'F' + str(i) + str(j)
            win_counter = 0
            for k in my_data.keys():
                if k == next_step:
                    board[i][j] = turn % 2
                    print('advance :', 'F' + str(i) + str(j),
                          'win :', max_win)
                    return 'F' + str(i) + str(j)

                if len(k) >= n + 3 and k[:n + 3] == next_step:
                    if my_data[k] == 1:
                        win_counter += 1
            if win_counter > max_win:
                step = [i, j]
                max_win = win_counter
    if len(step) > 0:
        board[step[0]][step[1]] = turn % 2
        print('advance :', 'F' + str(step[0]) + str(step[1]), 'win :', max_win)
        return 'F' + str(step[0]) + str(step[1])
    return random_choose(turn)


def random_receive(turn):
    while True:
        x = math.floor(random.random() * 3)
        y = math.floor(random.random() * 3)
        if board[x][y] == -1:
            board[x][y] = turn % 2
            return 'E' + str(x) + str(y)


def receive(turn):
    command = input('write your choice : ')
    while True:
        if not re.fullmatch('\\d\\s\\d', command):
            print('true pattern : digit digit')
            command = input('write your choice : ')
            continue
        x, y = list(map(int, command.split()))
        if x not in range(1, 4) or y not in range(1, 4):
            print('true digit : x > 0 & x < 4')
            command = input('write your choice : ')
            continue
        if board[x - 1][y - 1] != -1:
            print('this box is filled!!')
            command = input('write your choice : ')
            continue
        break
    x, y = list(map(int, command.split()))
    board[x - 1][y - 1] = turn % 2
    return 'E' + str(x - 1) + str(y - 1)


def check_winner():
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != -1:
            return False, board[i][0]

        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != -1:
            return False, board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != -1:
        return False, board[0][0]
    if board[1][1] == board[0][2] == board[2][0] and board[2][0] != -1:
        return False, board[2][0]
    draw = True
    for i in range(3):
        for j in range(3):
            if board[i][j] == -1:
                draw = False
    if draw:
        return False, -1
    return True, -1


def show_board():
    print('---------------')
    for i in range(3):
        for j in range(3):
            if board[i][j] != -1:
                print(board[i][j], end=' ')
                continue
            print('*', end=' ')
        print()
    print('---------------')


def restart_board():
    for i in range(3):
        for j in range(3):
            board[i][j] = -1


def learn(my_log, my_prize):
    print('learning ...')
    extra_data = my_log.replace('E', 'G').replace('F', 'E').replace('G', 'F')
    if my_prize > 0:
        if my_log not in data.keys():
            data[my_log] = 1
            pass
        clean_data(extra_data)
    elif my_prize < 0:
        if extra_data not in data.keys():
            data[extra_data] = 1
            pass
        clean_data(log)
    else:
        data[my_log] = data[extra_data] = 0


def clean_data(sub_log):
    print('clean data ...')
    print('kill data: ', sub_log)
    keys_arr = []
    for i in data.keys():
        if len(i) >= len(sub_log) and i[:len(sub_log) - 3] == sub_log[:len(
                sub_log) - 3]:
            keys_arr.append(i)
    for i in keys_arr:
        print(i)
        data.pop(i)
    # if len(keys_arr) > 0:
    # print('oh yes, good cleaning')
    # print(sub_log)


def main(my_data):
    winner = -1
    action_log = ''
    my_turn = math.floor(random.random() * 2)
    # print('my turn :', my_turn)
    turn = 0
    end = True
    while end:
        if turn % 2 == my_turn:
            action_log += advance_choose(turn, action_log, data)
        else:
            action_log += receive(turn)
        end, winner = check_winner()
        turn += 1
        show_board()
    if winner == my_turn:
        game_prize = 1
    elif winner == -1:
        game_prize = 0
    else:
        game_prize = -1
    return action_log, game_prize


counter_game = 1
data: map = read_data()

while counter_game > 0:
    log, prize = main(data)
    data = read_data()
    learn(log, prize)
    restart_board()
    counter_game -= 1
write_data(data)
