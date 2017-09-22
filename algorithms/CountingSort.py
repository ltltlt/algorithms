'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		CountingSort.py
  > Created Time:	2017-09-22 Fri 13:07
'''''''''''''''''''''''''''''''''''''''''''''''''''

" used when element in array in small range "
" time complexity O(n), stable"
def check(keys, low_bound, up_bound):
    class CheckError(Exception): pass
    for k in keys:
        if not low_bound<=k<up_bound:
            raise CheckError("{} not in [{}, {})".format(k, low_bound, up_bound))
def CountingSort(array, key=lambda x: x):
    keys = list(map(key, array))
    check(keys, 0, 256)

    R = 256

    counts = [0]*(R+1)      # never use counts[0]
    for k in keys:
        counts[k+1] += 1

    # calculate frequence, counts[i+1] stores i's frequence
    for i in range(1, R+1):
        counts[i] += counts[i-1]

    # put it
    result = [None]*len(array)
    for k, elem in zip(keys, array):
        # current place to put is the sum of previous frequence
        result[counts[k]] = elem
        counts[k] += 1       # the place to put, next same element should put in next place
    return result

def CountingSortUnstable(array, key=lambda x: x):
    '''
    unstable but more clear, according to <<introduction to algorithms>>
    '''
    keys = list(map(key, array))
    check(keys, 0, 256)

    counts = [0]*256
    for k in keys:
        counts[k] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i-1]
    result = [None]*len(array)
    for k, elem in zip(keys, array):
        counts[k] -= 1
        result[counts[k]] = elem
    return result
