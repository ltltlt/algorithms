'''
  > File Name: eight-queen.py
  > Author: ty-l
  > Mail: liuty196888@gmail.com
'''

import pdb
import _thread
import random
import sys
import threading

NUM = 8
number = 0
results = []
results_lock = _thread.allocate_lock()

def add_one_result(board):
    global number
    number += 1
    result = []
    for i in board:
        line = ['_']
        line = line * i + ['@'] + line * (NUM - i - 1)
        result.append(' '.join(line))
    with results_lock:
        results.append(result)
def check(*already_set_lst):
    for index1, line1 in enumerate(already_set_lst):
        for index2, line2 in enumerate(already_set_lst[:index1]):
            if line1 == line2 or abs(index1 - index2) == abs(line1 - line2):
                return False
    return True
def set_next_line(*already_set_lst):
    next_line = len(already_set_lst)
    if next_line >= NUM:
        add_one_result(already_set_lst)
    else:
        for i in range(NUM):
            if check(*already_set_lst, i):
                set_next_line(*already_set_lst, i)

def print_board(board):
    for line in board:
        print(line)
    print()
def print_one_result():
    random_generate = random.Random()
    with results_lock:
        index = random_generate.randint(0, len(results))
        print_board(results.pop(index))

def main_func():
    while True:
        line = input('>>>> ')
        if line == 'help':
            pass
        elif line == 'print':
            rnumber = int(input('number: '))
            if not rnumber: rnumber = 1
            for i in range(rnumber):
                print_one_result()
        elif line in ('exit', 'quit'):
            sys.exit(1)
        else:
            print('bad input')

thread1 = threading.Thread(target = set_next_line, args = ())
thread2 = threading.Thread(target = main_func, args = ())

thread1.start()
thread2.start()
