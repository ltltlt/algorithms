'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		binarySearch.py
  > Created Time:	2017-09-22 Fri 10:12
'''''''''''''''''''''''''''''''''''''''''''''''''''

def binarySearch(k, array):
    l, u = 0, len(array)-1
    while l<=u:
        # invariant: if k in array, then k in [l, u]
        m = (l+u)//2
        if array[m] > k:
            u = m-1
        elif array[m] < k:
            l = m+1
        else: return m
    # assert l==u+1
    return -l       # if not found, l is the index to insert k in array to keep array in sort
                    # at last, l must be the first element in array which is larger than k
def binarySearchRecursive(k, array):
    def recursive(k, array, l, u):
        if l>u: return -l
        m = (l+u)//2
        if array[m] > k:
            return recursive(k, array, l, m-1)
        elif array[m] < k:
            return recursive(k, array, m+1, u)
        else: return m
    return recursive(k, array, 0, len(array)-1)
