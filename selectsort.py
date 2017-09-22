'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		selectsort.py
  > Created Time:	2017-09-22 Fri 10:58
'''''''''''''''''''''''''''''''''''''''''''''''''''

# select sort using binarySearch written by lty, which time complexity is O(nlogn)

from binarySearch import binarySearch

def selectSort(array):
    result = []
    for elem in array:
        result.insert(abs(binarySearch(elem, result)), elem)
    return result

def normalSelectSort(array):
    length = len(array)
    if length<=1: return array
    for i in range(1, length):
        for j in range(i-1, 0, -1):
            if array[j]<array[i]:
                break
        array[i], array[j] = array[j], array[i]
    return array

def recursiveSelectSort(array, result):
    if len(result) >= len(array):
        return result
    elem = array[len(result)]
    result.insert(abs(binarySearch(elem, result)), elem)
    return recursiveSelectSort(array, result)
