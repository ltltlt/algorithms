'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Archlinux
  > Author:		ty-l6
  > Mail:		liuty196888@gmail.com
  > File Name:		trie.py
  > Created Time:	2017-09-24 Sun 18:46
'''''''''''''''''''''''''''''''''''''''''''''''''''

"String search tree(aka trie), quite fast but cost a lot of space."
"It can used as a map<string, ?> or set<string>."
"<<Algorithms>> using array to store child, so it need a R value indicate the size of alphabet"
"While i use a dict to store child, so i don't need R constant, childs can auto stretch."
"Because it's written by Python, so it is only for study use :)."

class TrieNode:
    def __init__(self):
        self.childs = dict()
        self.value = None
class TrieST:
    " Trie, all methods written without recursive, maybe sometime i will write every method using recursive. "
    def __init__(self, d=None):
        self.root = TrieNode()
        if d:
            [self.put(k, v) for k, v in d.items()]
    def check_key(self, key):
        assert type(key)==str and key, "key must be a str and should not be empty"
    def get(self, key):
        " call _get to get a node, then get it's value "
        node = self._get(key)
        return node.value if node else None
    def _get(self, key):
        " iterate get a node using key from tree "
        self.check_key(key)
        current = self.root
        for char in key:
            if char not in current.childs:
                return None
            current = current.childs[char]
        return current
    def put(self, key, value):
        " insert (key, value) into tree "
        self.check_key(key)
        assert value!=None, "value should not be None, or the result of get will confuse you"

        current = self.root
        for char in key:
            current = current.childs.setdefault(char, TrieNode())
        current.value = value
    def contains(self, key):
        " check if this tree contain this key "
        return self.get(key)!=None
    def isEmpty(self):
        " check if this tree is empty"
        return not bool(self.root)
    def longestPrefixOf(self, s):
        " the longest prefix of this string this tree contains "
        chars = []
        tmp = []
        current = self.root
        for char in s:
            if char not in current.childs:
                break
            current = current.childs[char]
            tmp.append(char)
            if current.value:
                chars.extend(tmp)
                tmp = []
        return ''.join(chars)
    def keysWithPrefix(self, s):
        " all keys prefix with s "
        return [key for key,_ in self.collect(self._get(s), prefix=s)]
    def collect(self, node, prefix=''):
        " collect all keys and values from this tree "
        " note that all keys appear randomly, because we use dict to store childs and dict is unordered"
        if node is None: return []
        stack = [(node, prefix)]
        pairs = []
        while stack:
            node, prefix = stack.pop()
            if node.value is not None:
                pairs.append((prefix, node.value))
            for char, child in node.childs.items():
                stack.append((child, prefix+char))
        return pairs
    def keys(self):
        " get all keys "
        return self.keysWithPrefix('')
    def values(self):
        " get all values "
        return [value for _, value in self.collect(self.root)]
    def items(self):
        " get all (key, value) pairs "
        return self.collect(self.root)
    def collectMatchPattern(self, node, pattern, prefix=''):
        " get all keys and values which key match pattern from this tree "
        if node is None: return []
        next_level_nodes = [(node, prefix)]
        for char in pattern:
            nodes, next_level_nodes = next_level_nodes, []
            for node, prefix in nodes:
                for c, child in node.childs.items():
                    if char in ('.', c):
                        next_level_nodes.append((child, prefix+c))
        return [(key, node.value) for node, key in next_level_nodes if node.value]
    def keysThatMatch(self, pattern):
        " get all keys match s. only . support, it means any one char "
        return [key for key, _ in self.collectMatchPattern(self.root, pattern)]
    def delete(self, key):
        " delete key, value from tree "
        " it needs to walk down the tree then walk up. use recursive it will be quite straightforword "
        " when we iterate, we need to record the path "
        self.check_key(key)
        paths = [(self.root, '')]
        for char in key:
            node, _  = paths[-1]
            if char not in node.childs:
                raise KeyError('{} not in trie tree'.format(key))
            paths.append((node.childs[char], char))
        # i am quite sorry that i wrote this shitty code
        paths[-1][0].value = None
        for i in range(len(paths)-1, 0, -1):
            (parent, _), (child, char) = paths[i-1:i+1]
            if child.value or child.childs:     # it have value or have child, stop delete
                break
            del parent.childs[char]
    def printTree(self):
        from collections import deque
        queue = deque([(self.root, '', '')])
        while queue:
            current, char, parent_char = queue.popleft()
            print('(char:{}, value:{}, parent_char:{})'.format(char, current.value, parent_char))
            for c, child in current.childs.items():
                queue.append((child, c, char))
