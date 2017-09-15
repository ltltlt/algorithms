'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		quicksort.py
  > Created Time:	2017-09-15 Fri 15:45
'''''''''''''''''''''''''''''''''''''''''''''''''''

def quicksort(array):
    def qsort(array):
        return qsort(list(filter(lambda x:x<array[0], array[1:])))+[array[0]]+qsort(list(filter(lambda x:x>=array[0], array[1:]))) if len(array)>1 else array
    return type(array)(qsort(list(array)))
