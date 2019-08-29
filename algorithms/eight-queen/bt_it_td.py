'''
  > File Name: iter.py
  > Author: ty-l
  > Mail: liuty196888@gmail.com
'''

import itertools
import threading
import sys
NUM = 11
num = 0
not_print = False
isOdd = NUM % 2

def print_board(arglist):
    global num
    num += 1
    if not_print:
        return
    for pos in arglist:
        print('_ ' * pos + '@ ' + (NUM - pos - 1) * '_ ')
    print()
def get_reverse_board(board):
    return [NUM-x-1 for x in board]
def check(arglist, pos):
    lenn = len(arglist)
    for index, i in enumerate(arglist):
        if i == pos or abs(i - pos) == lenn - index:
            return False
    return True
def nqueens():
    arglists = []
    n = (NUM//2+1) if isOdd else NUM//2
    for i in range(n):
        arglists.append([i])
    while arglists:
        arglist = arglists.pop()
        if len(arglist) == NUM:
            yield arglist
            if not isOdd or arglist[0] != (n - 1):
                yield get_reverse_board(arglist)
        else:
            for i in range(NUM):
                if check(arglist, i):
                    arglists.append(arglist + [i])

def main():
    solution = nqueens()
    while True:
        line = input('>>> ')
        if line == 'print':
            num = int(input('number: '))
            if not num:
                sys.exit(1)
            for i in range(num):
                print_board(next(solution))
        elif line == 'exit':
            sys.exit(0)
        elif line == 'num':
            print(len(list(nqueens())))
        else:
            print('bad input:', line)

if __name__ == '__main__':
    main()
