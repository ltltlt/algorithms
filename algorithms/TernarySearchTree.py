'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		TernarySearchTree.py
  > Created Time:	2017-09-26 Tue 10:21
'''''''''''''''''''''''''''''''''''''''''''''''''''

class TSTNode:
    def __init__(self, char):
        self.left = self.right = self.mid = None
        self.value = None
        self.char = char
class TernarySearchTree:
    def __init__(self, d):
        self.root = None
        if d: [self.put(k, v) for k, v in d.items()]
    def check_key(self, key):
        assert type(key)==str and key, "key must be a str and should not be empty"
    def put(self, key, value):
        " put key and value into this tree, it's not as clean as code written by recursive "
        self.check_key(key)
        assert value!=None, "value must not be None or you will get confused"
        if not self.root: self.root = TSTNode(key[0])

        def goToChild(current, which, char):
            if not current.__dict__[which]:
                current.__dict__[which] = TSTNode(char)
            return current.__dict__[which]
        current = self.root
        i = 0
        while i < len(key)-1:
            char = key[i]
            if char > current.char:
                current = goToChild(current, 'right', key[i])
            elif char < current.char:
                current = goToChild(current, 'left', key[i])
            else:
                current = goToChild(current, 'mid', key[i+1])
                i += 1
        current.value = value
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
        " delete key, value from tree "
        " the hardest part comes, i still have no idea what should i do about delete "
        self.check_key(key)
        paths = [(self.root, '')]
        i = 0
        while i < len(key):
            node, _ = paths[-1]
            if node is None: raise KeyError("{} is not exist".format(key))
            if key[i] == node.char:
                paths.append((node.mid, 'mid'))
                i += 1
            elif key[i] < node.char:
                paths.append(node.left, 'left')
            elif key[i] > node.char:
                paths.append(node.right, 'right')
        paths[-1][0].mid = paths[-1][0].value = None
        for i in range(len(paths)-1, 0, -1):
            (parent, _), (child, which) = paths[i-1:i+1]    # parent.which is child
            if child.mid or paths[-1][0].value: break
            if which in ('left', 'right'):
                parent.__dict__[which] = None
            else:
                self.complexDelete(parent):  # it must be parent.mid need to delete
    def complexDelete(self, parent):
        " it't quite complex, so i call it complexDelete "
        " just like delete a node in binary tree "
        child = parent.mid
        if not child.left and not child.right:
            parent.mid = None
        elif not child.left and child.right:
            parent.mid = child.right
        elif child.left and not child.right:
            parent.mid = child.left
        else:   # both left and right exists
            # find child's successor
            parent_of_succ, successor = self.findSuccessor(child)
            parent.mid = successor
            successor.left = child.left
            if parent_of_succ is not child: # successor is not child.right
                successor.right = child.right
                parent_of_succ.left = None  # delete it
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
        return [key for key, _ in self.collect(self._get(s), prefix=s)]
    def collect(self, node, prefix=''):
        " collect all keys and values from this subtree(which root is node) "
        if node is None: return []
        stack = [(node, prefix)]
        pairs = []
        while stack:
            node, prefix = stack.pop()
            if node.value is not None:
                pairs.append((prefix, node.value))
            stack.extend([(node.left, prefix),\
                    (node.right, prefix), (node.mid, prefix+char)])
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
        if pattern == '':
            if node.value:
                return [(prefix, node.value)]
            else: return []
        result = []
        if pattern[0] < node.char or pattern[0]=='.':
            result.extend(self.collectMatchPattern(node.left, pattern, prefix=prefix))
        if pattern[0] > node.char or pattern[0]=='.':
            result.extend(self.collectMatchPattern(node.right, pattern, prefix=prefix))
        if pattern[0] in (node.char, '.'):
            result.extend(self.collectMatchPattern(node.mid, pattern[1:], prefix=prefix+node.char))
        return result
    def collectMatchPatternIterate(self, node, pattern, prefix=''):
        " as long as stack store enough information, all tail recursive can convert into iterate "
        if node is None: return []
        stack = [(node, prefix, pattern)]
        results = []
        while stack:
            node, prefix, pattern = stack.pop()
            if pattern == '':
                if node.value:
                    results.append((prefix, node.value))
                continue
            if pattern[0] < node.char or pattern[0]=='.':
                stack.append((node.left, pattern, prefix))
            if pattern[0] > node.char or pattern[0]=='.':
                stack.append((node.right, pattern, prefix))
            if pattern[0] in ('.', node.char):
                stack.append((node.mid, pattern[1:], prefix+node.char))
        return results
    def keysThatMatch(self, pattern):
        return self.collectMatchPattern(self.root, pattern)
    def printTree(self):
        pass
