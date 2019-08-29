'''
  > File Name: eight-queen.py
  > Author: ty-l
  > Mail: liuty196888@gmail.com
'''

import pdb

NUM = 10
number = 0
printp = False

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
def check(*already_set_lst):
    for index1, line1 in enumerate(already_set_lst):
        for index2, line2 in enumerate(already_set_lst[:index1]):
            if line1 == line2 or abs(index1 - index2) == abs(line1 - line2):
                return False
    return True
def set_next_line(*already_set_lst):
    next_line = len(already_set_lst)
    if next_line >= NUM:
        print_board(already_set_lst)
    else:
        for i in range(NUM):
            if check(*already_set_lst, i):
                set_next_line(*already_set_lst, i)

set_next_line()
print('total have: ', number)
