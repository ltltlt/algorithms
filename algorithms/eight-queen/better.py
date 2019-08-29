'''
  > File Name: eight-queen.py
  > Author: ty-l
  > Mail: liuty196888@gmail.com
'''

import pdb
import math

NUM = 11
number = 0
printp = False
NUMisODD = NUM % 2

def print_board(board):
    global number
    number += 1
    if not printp:
        return
    for i in board:
        line = ['_']
        line = line * i + ['@'] + line * (NUM - i - 1)
        print(' '.join(line))
    print()
def print_reverse_board(board):
    print_board([NUM-i-1 for i in board])
def check(*already_set_lst):
    for index1, line1 in enumerate(already_set_lst):
        for index2, line2 in enumerate(already_set_lst[:index1]):
            diat1 = index1 - index2
            diat2 = line2 - line1
            if diat2 == 0 or diat1 == diat2 or -diat2 == diat1:
                return False
    return True
def set_next_line(*already_set_lst, half=False):
    next_line = len(already_set_lst)
    if next_line >= NUM:
        print_board(already_set_lst)
        if not NUMisODD or already_set_lst[0] != NUM//2:
            print_reverse_board(already_set_lst)

    else:
        size = math.ceil(NUM/2) if half else NUM
        for i in range(size):
            if check(*already_set_lst, i):
                set_next_line(*already_set_lst, i)

if __name__ == '__main__':
    set_next_line(half=True)
    print('total have: ', number)
