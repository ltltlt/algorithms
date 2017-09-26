'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		TernarySearchTree.py
  > Created Time:	2017-09-26 Tue 10:21
'''''''''''''''''''''''''''''''''''''''''''''''''''

import sys
class TSTNode:
    def __init__(self, char):
        self.left = self.right = self.mid = None
        self.value = None
        self.char = char
    def __repr__(self):
        representation = '(char: {}) (value: {})'.format(self.char, self.value)
        if self.left:
            representation += '(left: {})'.format(self.left)
        if self.mid:
            representation += '(mid: {})'.format(self.mid)
        if self.right:
            representation += '(right: {})'.format(self.right)
        return representation
class TernarySearchTree:
    def __init__(self, d=None):
        self.root = None
        if d: [self.put(k, v) for k, v in d.items()]
    def check_key(self, key):
        assert type(key)==str and key, "key must be a str and should not be empty"
    def put(self, key, value):
        " put key and value into this tree, it's not as clean as code written by recursive "
        " after i wrote this method, i find it's just like the recursive version represent in Sedgewick's book "
        self.check_key(key)
        assert value!=None, "value must not be None or you will get confused"
        if not self.root: self.root = TSTNode(key[0])

        def goToChild(current, which, char):
            if not current.__dict__[which]:
                current.__dict__[which] = TSTNode(char)
            return current.__dict__[which]
        current = self.root
        i = 0
        while i < len(key):
            char = key[i]
            if char > current.char:
                current = goToChild(current, 'right', key[i])
            elif char < current.char:
                current = goToChild(current, 'left', key[i])
            else:
                if i<len(key)-1:
                    current = goToChild(current, 'mid', key[i+1])
                else: 
                    current.value = value
                i += 1
    def get(self, key):
        " get value by key "
        node = self._get(key)
        return node.value if node is not None else None
    def _get(self, key):
        " get node by key "
        self.check_key(key)
        current = self.root
        i = 0
        while i < len(key):
            char = key[i]
            if not current:
                return None
            result = current
            if char > current.char:
                current = current.right
            elif char < current.char:
                current = current.left
            else:
                current = current.mid
                i += 1
        return result
    def delete(self, key):
        " delete key, value from tree, and return value "
        " the hardest part comes, i still have no idea what should i do about delete "
        self.check_key(key)
        paths = [(self.root, '')]
        i = 0
        while i < len(key):
            node, _ = paths[-1]
            if node is None: raise KeyError("Key {} doesn't exist".format(key))
            if key[i] == node.char:
                paths.append((node.mid, 'mid'))
                i += 1
            elif key[i] < node.char:
                paths.append((node.left, 'left'))
            elif key[i] > node.char:
                paths.append((node.right, 'right'))
        paths.pop()     # last one is (None, 'mid')
        if paths[-1][0].value is None:
            raise KeyError("Key {} doesn't exist".format(key))
        result, paths[-1][0].value = paths[-1][0].value, None
        for i in range(len(paths)-1, 0, -1):
            (parent, _), (child, which) = paths[i-1:i+1]    # parent.which is child
            if child.mid or child.value: break   # if it's mid is not None, break
            self.complexDelete(parent, which)
        if self.root.value == self.root.mid == None:    # the for loop will not delete root, but maybe we want to
            node = TSTNode('1')     # complexDelete is just right, so i don't want to change it
            node.mid = self.root
            self.complexDelete(node, 'mid')
            self.root = node.mid
        return result
    def complexDelete(self, parent, which):
        " it't quite complex, so i call it complexDelete "
        " just like delete a node in binary tree "
        child = parent.__dict__[which]
        if not child.left and not child.right:
            parent.__dict__[which] = None
        elif not child.left and child.right:
            parent.__dict__[which] = child.right
        elif child.left and not child.right:
            parent.__dict__[which] = child.left
        else:   # both left and right exists
            # find child's successor
            parent_of_succ, successor = self.findSuccessor(child)
            parent.__dict__[which] = successor
            successor.left = child.left
            if parent_of_succ is not child: # successor is not child.right
                parent_of_succ.left = successor.right
                successor.right = child.right
            # child should not have mid, or why will we delete it
    def findSuccessor(self, node):
        " :node TSTNode, the node we want to find it's successor"
        " :rtype tuple(father_of_successor, successor)"
        assert type(node)==TSTNode, "node should be a TSTNode"
        prev = node
        current = node.right
        while current.left:
            prev = current
            current = current.left
        return prev, current
    def contains(self, key):
        " check if this tree contains this key "
        return self.get(key) is not None
    def isEmpty(self):
        " check if this tree is empty "
        return self.root is None
    def longestPrefixOf(self, s):
        " the longest prefix of this string this tree contains "
        chars, tmp = [], []
        current = self.root
        i = 0
        while current and i<len(s):
            if s[i] == current.char:
                tmp.append(current.char)
                if current.value:
                    chars.extend(tmp)
                i, current = i+1, current.mid
            elif s[i] < current.char:
                current = current.left
            else: current = current.right
        return ''.join(chars)
    def keysWithPrefix(self, s):
        " all keys prefix with s "
        node = self._get(s)
        result = []
        if node.value:
            result = [s]
        else: result = []
        return result + [key for key, _ in self.collect(node.mid, prefix=s)]
    def collect(self, node, prefix=''):
        " collect all keys and values from this subtree(which root is node) "
        if node is None: return []
        stack = [(node, prefix)]
        pairs = []
        while stack:
            node, prefix = stack.pop()
            if node is None: continue
            if node.value is not None:
                pairs.append((prefix+node.char, node.value))
            stack.extend([(node.left, prefix),\
                    (node.right, prefix), (node.mid, prefix+node.char)])
        return pairs
    def keys(self):
        " get all keys "
        return [key for key, _ in self.collect(self.root)]
    def values(self):
        " get all values "
        return [value for _, value in self.collect(self.root)]
    def items(self):
        " get all kv pairs "
        return self.collect(self.root)
    def collectMatchPattern(self, node, pattern, prefix=''):
        " get all keys and values which key match pattern from this tree from subtree "
        " i wrote recursive then according it, i wrote iterate version, and yes, i am suck"
        if node is None: return []
        self.check_key(pattern)
        result = []
        if pattern[0]=='.' or pattern[0] < node.char:
            result.extend(self.collectMatchPattern(node.left, pattern, prefix=prefix))
        if pattern[0]=='.' or pattern[0] > node.char:
            result.extend(self.collectMatchPattern(node.right, pattern, prefix=prefix))
        if pattern[0] in (node.char, '.'):
            prefix = prefix + node.char
            if len(pattern)==1:
                if node.value:
                    result.append((prefix, node.value))
            else:
                result.extend(self.collectMatchPattern(node.mid, \
                        pattern[1:], prefix=prefix))
        return result
    def collectMatchPatternIterate(self, node, pattern, prefix=''):
        " as long as stack store enough information, all tail recursive can convert into iterate "
        self.check_key(pattern)
        stack = [(node, pattern, prefix)]
        results = []
        while stack:
            node, pattern, prefix = stack.pop()
            if node is None: continue
            if pattern[0]=='.' or pattern[0]<node.char:
                stack.append((node.left, pattern, prefix))
            if pattern[0]=='.' or pattern[0]>node.char:
                stack.append((node.right, pattern, prefix))
            if pattern[0] in ('.', node.char):
                prefix = prefix + node.char
                if len(pattern)==1:
                    if node.value:
                        results.append((prefix, node.value))
                else:
                    stack.append((node.mid, pattern[1:], prefix))
        return results
    def keysThatMatch(self, pattern):
        return self.collectMatchPatternIterate(self.root, pattern)
    def printTree(self, file=sys.stdout):
        from collections import deque
        queue = deque([(self.root, None, '')])
        while queue:
            current, parent, which = queue.popleft()
            if not current: continue
            print('(char:{}, value:{}, parent:{}->{})'.format(current.char, current.value,\
                    parent.char if parent else '', which), file=file)
            queue.extend([
                (current.left, current, 'left'),
                (current.mid, current, 'mid'),
                (current.right, current, 'right')
                ])
    def __repr__(self):
        from io import StringIO
        sio = StringIO()
        self.printTree(file=sio)
        return sio.getvalue()
