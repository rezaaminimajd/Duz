import json
import random
import math
import re

board = [[-1, -1, -1], [-1, -1, -1], [-1, -1, -1]]


def read_data():
    with open('data.json', 'r') as f:
        return json.load(f)


def write_data(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)


def random_choose(turn):
    while True:
        x = math.floor(random.random() * 3)
        y = math.floor(random.random() * 3)
        if board[x][y] == -1:
            board[x][y] = turn % 2
            return 'F' + str(x) + str(y)


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

    return True, -1


def show_board():
    for i in range(3):
        for j in range(3):
            print(board[i][j], end=' ')
        print()


def main():
    data: map = read_data()
    winner = -1
    action_log = ''
    my_turn = math.floor(random.random() * 2)
    turn = 0
    end = True
    while end:
        if turn % 2 == my_turn:
            action_log += random_choose(turn)
            show_board()
        else:
            action_log += receive(turn)
        end, winner = check_winner()
        turn += 1
    if winner == my_turn:
        game_prize = 1
    elif winner == -1:
        game_prize = 0
    else:
        game_prize = -1
    return data, action_log, game_prize


my_map, log, prize = main()
if log in my_map.keys():
    my_map[log] += prize
else:
    my_map[log] = prize
extra_data = log.replace('E', 'G').replace('F', 'E').replace('G', 'F')
extra_data_prize = -1 * prize
if extra_data in my_map.keys():
    my_map[extra_data] += extra_data_prize
else:
    my_map[extra_data] = extra_data_prize

write_data(my_map)
