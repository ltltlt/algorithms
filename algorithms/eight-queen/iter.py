'''
  > File Name: iter.py
  > Author: ty-l
  > Mail: liuty196888@gmail.com
'''

import itertools
NUM = 8
num = 0
not_print = True

def print_board(arglist):
    global num
    num += 1
    if not_print:
        return
    for pos in arglist:
        print('_ ' * pos + '@ ' + (NUM - pos -1) * '_ ')
    print()
def check(arglist, i):
    for j in range(len(arglist)):
        if abs(arglist[j] - i) in (0, len(arglist) - j):
            return False
    return True
def nqueens():
    arglists = [[]]
    while arglists:
        arglist = arglists.pop()
        if len(arglist) == NUM:
            print_board(arglist)
        else:
            arglists.extend(arglist + [i] for i in range(NUM) if check(arglist, i))

nqueens()
print(num)
