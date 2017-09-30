'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Chrome
  > Author:		ty-l9
  > Mail:		liuty196888@gmail.com
  > File Name:		KMP.py
  > Created Time:	2017-09-29 Fri 23:29
'''''''''''''''''''''''''''''''''''''''''''''''''''
" i almost understand KMP, but something still not clear, and what is something is not clear... "
" and i cannot write the right version of save space KMP, maybe i need some break. "

from basic import BasicSubStringSearch

class KMP(BasicSubStringSearch):
    def __init__(self, pattern):
        super().__init__(pattern)
        self.create_dfa()
    def process(self, string):
        dfa = self.dfa
        pattern = self.pattern
        n, m = len(string), len(pattern)
        i, j = 0, 0 
        while i<n and j<m:          # simulate automaten run
            j = dfa[ord(string[i])][j]
            i += 1
        if j == m:      # found substring
            return i-m  # begin of pattern occur
        else:       # i == n
            return n
    def create_dfa_the_hard_way(self):
        " easy to understand version "
        pattern = self.pattern
        dfa = [ [0]*len(pattern) for i in range(self.alphabetLen) ]    # row is alphabetLen, column is status
        dfa[ord(pattern[0])][0] = 1
        for j in range(1, len(pattern)):       # for each status
            # string[i] != pattern[j], we just need dfa to go back to some status
            # we have string[i-j:i]==pattern[0:j], we need to see string[i-j+1:i](aka pattern[1:j]) lead new DFS to what status
            # we don't include pattern[0] because if so, we go back to current status again
            # we don't include string[i] because we don't know what it is(!=pattern[j])
                # also, in current status, string[i] will lead to just the same status as if current status is δ(status0, pattern[1:j])
                # so we just need copy dfa[][δ(status0, pattern[1:j])] to dfa[][current_status]
            substr = pattern[1:j]  # exclude 1 because we don't want to get the same result, exclude i because we use this char to go back
            # see what status substr lead automaten to
            status = 0      # begin status
            for c in substr:
                status = dfa[ord(c)][status]
            # copy dfa[][status] to dfa[][j]
            for k in range(self.alphabetLen):
                dfa[k][j] = dfa[k][status]

            # string[i] == pattern[j], only one char will match(eg, string[i], pattern[j])
            dfa[ord(pattern[j])][j] = j+1       # in the match case, we go to next status
        self.dfa = dfa
    def create_dfa(self):
        pattern = self.pattern
        dfa = [ [0]*len(pattern) for i in range(self.alphabetLen) ]
        dfa[ord(pattern[0])][0] = 1
        status = 0
        for j in range(1, len(pattern)):    # status <= j always true
            for k in range(self.alphabetLen):
                dfa[k][j] = dfa[k][status]
            dfa[ord(pattern[j])][j] = j+1
            # notice that in create_dfa_the_hard_way, substr always include pattern[1...], so we can make status calculate more faster
            status = dfa[ord(pattern[j])][status]
        self.dfa = dfa

# don't use the two below, i am quite certain they are mistake
# i try to connect DFA to next array, and i have trouble at go back status calculate
# i will fix it in the future, when i have the ability to deal with it
class SpaceOptimize(KMP):
    # in fact, we just need to record two next status for every status
    # one for match, it will be next status, and one for unmatch, for this situation, we don't add i
    # because dfa still need string[i] to goto some status
    def process(self, string):
        pattern = self.pattern
        dfa = self.dfa
        n, m = len(string), len(pattern)
        i, j = 0, 0
        while i<n and j<m:
            if pattern[j] == string[i]:
                i, j = i+1, dfa[j][0]
            else:
                j = dfa[j][1]
        if j == m: return i-m
        else: return n
    def create_dfa(self):
        pattern = self.pattern
        dfa = [ [0, 0] for i in range(len(pattern)) ]       # a little change, now row is status, column 0 is match, column 1 is unmatch
        dfa[0][0] = 1       # pattern[0] match(0 match, 1 unmatch)
        status = 0
        for j in range(1, len(pattern)):
            substr = pattern[1:j]
            i, k = 0, 0
            while i < len(substr) and k < len(pattern):
                if pattern[k] == substr[i]:
                    i, k = i+1, dfa[k][0]
                else: k = dfa[k][1]
            status = k
            dfa[j] = j+1, status
        self.dfa = dfa
class SpaceOptimize2(KMP):
    # we can make space even smaller, because we don't need dfa columns 0(match)
    # here, dfa become 1 dimention array, someone would like to call it `next` array
    def process(self, string):
        pattern = self.pattern
        dfa = self.dfa
        n, m = len(string), len(pattern)
        i, j = 0, 0
        while i<n and j<m:
            if pattern[j] == string[i]:
                i, j = i+1, j+1
            else: j = dfa[j]
        if j == m: return i-m
        else: return n
    def create_dfa(self):
        pattern = self.pattern
        dfa = [0]*len(pattern)
        status = 0
        for j in range(1, len(pattern)):
            substr = pattern[1:j]
            i, k = 0, 0
            while i<len(substr) and k<len(pattern):
                if pattern[k] == substr[i]:
                    i, k = i+1, k+1
                else: k = dfa[k]
            status = k
            dfa[j] = status
        self.dfa = dfa
