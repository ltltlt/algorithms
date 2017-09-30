'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Chrome
  > Author:		ty-l9
  > Mail:		liuty196888@gmail.com
  > File Name:		test.py
  > Created Time:	2017-09-30 Sat 23:25
'''''''''''''''''''''''''''''''''''''''''''''''''''

from Robin_Karp import Robin_Karp
from simpleBoyerMoore import BoyerMoore
from KMP import KMP
from random import sample, randrange
from string import printable

def get_txt(size):
    txt = []
    for _ in range(size):
        txt.extend(sample(printable, 1))
    return ''.join(txt)
def test(case, cls, min_txt_size=100, max_txt_size=1000):
    for _ in range(case):
        txt_size = randrange(min_txt_size, max_txt_size)
        txt = get_txt(txt_size)
        for size in range(1, txt_size//4):
            pattern = get_txt(size)
            r1 = cls(pattern).process(txt)
            if r1 == txt_size: r1 = -1
            r2 = txt.find(pattern)
            assert r1 == r2, '{}(txt: {} pattern: {}, robin_karp: {}, find: {})'.format(cls.__name__, txt, pattern, r1, r2)
if __name__ == '__main__':
    test(200, BoyerMoore)
    test(200, Robin_Karp)
    test(200, KMP)
