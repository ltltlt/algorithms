'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Chrome
  > Author:		ty-l9
  > Mail:		liuty196888@gmail.com
  > File Name:		simpleBoyerMoore.py
  > Created Time:	2017-09-30 Sat 19:22
'''''''''''''''''''''''''''''''''''''''''''''''''''
" as the name implys, this is quite simple, just like the one in <<Algorithms>>. "
" and this is slower then normal one, because we don't skip much "

from basic import BasicSubStringSearch
class BoyerMoore(BasicSubStringSearch):
    def __init__(self, pattern):
        super().__init__(pattern)
        right = [-1]*256        # if char never appear in pattern, it's -1(this will make thing much easier)
        for i in range(len(pattern)):
            right[ord(pattern[i])] = i
        self.right = right
    def process(self, string):
        pattern, right = self.pattern, self.right
        n, m = len(string), len(pattern)
        if n<m: return n
        i = 0
        while i+m <= n:
            for j in range(m-1, -1, -1):
                if pattern[j] != string[i+j]:
                    break
            else:
                return i
            # we don't just let i = i+1, we skip some, it depends on right array
            # if right[..] is -1, we need to skip j+1(then i==i+j+1), because string[i+j] is not in pattern
            # if right[..] is >=0, which means string[i+j] the right side occur in pattern[right[..]], skip some, we let it align
            skip = j-right[ord(string[i+j])] 
            # if skip < 1, which means the right most string[i+j] occur in right side of j, we just move i to next(like brute-force)
            if skip < 1: skip = 1
            i += skip
        return n
