'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Chrome
  > Author:		ty-l9
  > Mail:		liuty196888@gmail.com
  > File Name:		basic.py
  > Created Time:	2017-09-30 Sat 21:53
'''''''''''''''''''''''''''''''''''''''''''''''''''

from abc import abstractmethod

class BasicSubStringSearch:
    def __init__(self, pattern):
        assert pattern != '', 'pattern should not be empty, what the hell are you thinking???'
        self.pattern = pattern
        self.alphabetLen = 256      # you can change increate alphabetLen to fit in unicode
    @abstractmethod
    def process(self, string):
        """
        :string str
        :rtype int
        search pattern from string, if found, return index, else return n
        """
        pass
    def pretify(self, string, *args, **kwargs):
        """
        :string str
        call process method to get an index, use this index to pretify output
        """
        index = self.process(string, *args, **kwargs)
        if index == len(string):
            print(self.pattern, 'not found in', string)
            return
        print(string)
        if isinstance(index, int):
            print(' '*index+self.pattern)
        else:
            for i in index:
                print(' '*index+self.pattern)
