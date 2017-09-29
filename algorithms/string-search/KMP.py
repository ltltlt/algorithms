'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Chrome
  > Author:		ty-l9
  > Mail:		liuty196888@gmail.com
  > File Name:		KMP.py
  > Created Time:	2017-09-29 Fri 23:29
'''''''''''''''''''''''''''''''''''''''''''''''''''

class KMP:
    def __init__(self, pattern):
        self.alphabet_len = 256      # length of alphabet, you can change this to support unicode
        self.pattern = pattern
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
        dfa = [ [0]*len(pattern) for i in range(self.alphabet_len) ]    # row is alphabet_len, column is length of pattern
        for j in range(1, len(pattern)):       # for each status
            # string[i] != pattern[j], we just need dfa to go back to some status
            # we have string[i-j:i]==pattern[0:j], we need to see string[i-j+1:i](aka pattern[1:j]) lead new DFS to what status
            # we don't include pattern[0] because if so, we go back to current status again
            # we don't include string[i] because we don't know what it is(!=pattern[j])
                # also, string[i] will lead current DFS go back, we already go back, so we don't need it
            substr = pattern[1:j]  # exclude 1 because we don't want to get the same result, exclude i because we use this char to go back
            # see what status substr lead automaten to
            status = 0      # begin status
            for c in substr:
                status = dfa[ord(c)][status]
            # copy dfa[][status] to dfa[][j]
            for k in range(self.alphabet_len):
                dfa[k][j] = dfa[k][status]

            # string[i] == pattern[j], only one char will match(eg, string[i], pattern[j])
            dfa[ord(pattern[j])][j] = j+1       # in the match case, we go to next status
        self.dfa = dfa
    def create_dfa(self):
        pattern = self.pattern
        dfa = [ 0*len(pattern) for i in range(self.alphabet_len) ]
        status = 0
        for j in range(1, len(pattern)):    # status <= j always true
            for k in range(self.alphabet_len):
                dfa[k][j] = dfa[k][status]
            # notice that in create_dfa_the_hard_way, substr always include pattern[1...], so we can make status calculate more faster
            status = dfa[ord(pattern[j])][status]
        self.dfa = dfa
