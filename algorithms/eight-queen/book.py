'''
  > File Name: book.py
  > Author: ty-l
  > Mail: liuty196888@gmail.com
'''

def conflict(state, pos):
    lenn = len(state)
    for i in range(lenn):
        if abs(pos - state[i]) in (0 , lenn - i):
            return True
    return False

def queens(num = 11, state = ()):
    for i in range(num):
        if not conflict(state, i):
            if len(state) == num-1:
                yield (i,)
            else:
                for result in queens(state=state+(i,)):
                    yield (i, )+result

print(len(list(queens())))
