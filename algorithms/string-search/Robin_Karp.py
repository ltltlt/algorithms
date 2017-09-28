'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		Robin_Karp.py
  > Created Time:	2017-09-28 Thu 17:29
'''''''''''''''''''''''''''''''''''''''''''''''''''

' Use rolling hash, quite easy to understand(especially compares to KMP) '

def mod(a, b):
    ' calculate a%b, no matter a is negative or positive, return positive '
    return a%b      # in python, this works just right, but in some other language(like C++), you may need ((a%b)+b)%b
def LasVegas(str1, str2):
    " ensure the result is always right "
    return str1 == str2
def MonteCarlo(str1, str2):
    " ensure the time complexity is O(m+n) "
    return True
class Robin_Karp:
    def __init__(self, pattern):
        self.pattern = pattern
    def process(self, string, check=MonteCarlo, hash_num=1):    # find first occurance of pattern in string
        " find all pattern from string, string and pattern should be sequence of ascii "
        " you can surely change base to make it fit unicode "
        " remember even though hash value are the same, doesn't mean two string are the same, it just means they are highly likely the same "
        " you can provide check function to make sure two string are the same, or change hash_num to make it highly unlikely not the same "
        pattern = self.pattern
        bases = list(range(129, 129+hash_num))
        Ms = list(range(100001623, 100001623+hash_num))
        n, m = len(string), len(pattern)

        pat_hashs, hashs = [0]*hash_num, [0]*hash_num
        for i in range(m):
            for j in range(hash_num):
                pat_hashs[j] = pat_hashs[j]*bases[j]+ord(pattern[i])
                pat_hashs[j] = mod(pat_hashs[j], Ms[j])
                hashs[j] = hashs[j]*bases[j] + ord(string[i])
                hashs[j] = mod(hashs[j], Ms[j])
        if pat_hashs == hashs and check(pattern, string[:m]):
            return 0

        for i in range(1, n-m+1):
            for j in range(hash_num):
                hashs[j] = hashs[j]-ord(string[i-1])*pow(bases[j], m-1)
                hashs[j] = mod(mod(hashs[j], Ms[j])*bases[j] + ord(string[i+m-1]), Ms[j])
            if hashs == pat_hashs and check(pattern, string[i:i+m]):
                return i
    def pretify(self, *args, **kwargs):
        index = self.process(*args, **kwargs)
        if index is None:
            print('Not found!')
        else:
            print(*args)
            print(' '*index+self.pattern)
