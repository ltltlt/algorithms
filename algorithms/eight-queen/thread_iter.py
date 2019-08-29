'''
  > File Name: iter.py
  > Author: ty-l
  > Mail: liuty196888@gmail.com
'''

import threading

NUM = 12
num = 0
not_print = True
isOdd = NUM % 2
lock = threading.Lock()

def print_board(arglist):
    lock.acquire()
    global num
    num += 1
    if not not_print:
        for pos in arglist:
            print('_ ' * pos + '@ ' + (NUM - pos - 1) * '_ ')
        print()
    lock.release()
def print_reverse_board(board):
    print_board([NUM-x-1 for x in board])
def check(arglist, pos):
    length = len(arglist)
    for index, i in enumerate(arglist):
        diatcolumn, diatrow = i - pos, length - index
        if diatcolumn == 0 or diatcolumn == diatrow or diatcolumn == -diatrow:
            return False
    return True
def process(arglist):
    arglists = [arglist]
    if not isOdd or arglist[0] != NUM//2:
        reverse = False
    else:
        reverse = True
    while arglists:
        arglist = arglists.pop()
        if len(arglist) == NUM:
            print_board(arglist)
            if not reverse:
                print_reverse_board(arglist)
        else:
            arglists.extend(arglist + [i] for i in range(NUM) if check(arglist, i))
def nqueens():
    n = (NUM//2+1) if isOdd else NUM//2
    threads = [threading.Thread(target = process, args = ([x],)) for x in range(n)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    nqueens()
    print(num)
