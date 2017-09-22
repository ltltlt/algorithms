'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		mergeSort.py
  > Created Time:	2017-09-22 Fri 10:30
'''''''''''''''''''''''''''''''''''''''''''''''''''

from collections import deque

def merge(array1, array2):
    if not array1: return array2
    if not array2: return array1
    result = []
    i, j = 0, 0
    while i<len(array1) and j<len(array2):
        if array1[i]<array2[j]:
            result.append(array1[i])
            i+=1
        else:
            result.append(array2[j])
            j+=1
    if i>=len(array1): result.extend(array2[j:])
    else: result.extend(array1[i:])
    return result
def iterate(array):
    d = deque()
    for elem in array:
        d.append([elem])
    while len(d) > 1:
        merge_result = merge(d.popleft(), d.popleft())
        d.append(merge_result)
    try:
        return d.pop()
    except IndexError:
        return []
def recursive(array):
    if len(array)<=1:
        return array
    m = len(array)//2
    return merge(recursive(array[0:m]), recursive(array[m:]))

def test(sort_func):
    from random import randrange
    from copy import deepcopy
    for i in range(100):
        array = []
        for j in range(i):
            array.append(randrange(1000))
        array1 = deepcopy(array)
        array1.sort()
        assert sort_func(array) == array1, '{} {} {}'.format(array, sort_func(array), array1, array)
