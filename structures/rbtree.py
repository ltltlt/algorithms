'''''''''''''''''''''''''''''''''''''''''''''''''''
  > System:		Ubuntu
  > Author:		ty-l8
  > Mail:		liuty196888@gmail.com
  > File Name:		rbtree.py
  > Created Time:	2017-09-01 Fri 12:31
'''''''''''''''''''''''''''''''''''''''''''''''''''

class RbNode:
    p = None        # parent
    left = None
    right = None
    key = object()
    color = 'black'
    def __init__(self, key, left=None, right=None, p=None, color='black'):
        self.key = key
        self.left, self.right = left, right
        self.p = p
        self.color = color
    def __repr__(self):
        return '<RbNode {} @{}>'.format(self.key, id(self))
        
class RbTree:
    # note: it's very subtle that nil.p may change, keep it in mind
    @property
    def nil(self):
        node = getattr(self, '_nil_node', None)
        if node:
            return node
        nil = RbNode('nil')
        nil.left = nil.right = nil.p = nil
        nil.color = 'black'
        self._nil_node = nil
        return nil
    def __init__(self, iterator=None):
        self.root = self.nil
        if iterator:
            for i in iterator:
                self.rb_insert(i)
        
    def left_rotate(self, x):
        y = x.right
        x.right = y.left        # x
        y.p = x.p               # y
        if x.p is self.nil:     # x.p
            self.root = y
        elif x is x.p.left:
            x.p.left = y
        else:
            x.p.right = y
        if y.left:              # y.left
            y.left.p = x
        y.left = x              # y
        x.p = y                 # x
    def right_rotate(self, y):
        x = y.left
        y.left = x.right        # y
        x.p = y.p               # x
        if y.p is self.nil:     # y.p
            self.root = x
        elif y.p.left is y:
            y.p.left = x
        else:
            y.p.right = x
        if x.right:             # x.right
            x.right.p = y
        x.right = y             # x
        y.p = x                 # y
    
    def rb_insert(self, key):
        current = self.root
        parent = self.nil
        while current is not self.nil:
            parent = current
            if current.key > key:
                current = current.left
            else:
                current = current.right
        if parent is self.nil:          # self.root is self.nil
            newNode = RbNode(key=key, color='red', p=self.nil, left=self.nil, right=self.nil)
            self.root = newNode
        else:
            newNode = RbNode(key=key, p=parent, color='red', left=self.nil, right=self.nil)
            if key > parent.key:
                parent.right = newNode
            else: parent.left = newNode
        self.rb_insert_fixup(newNode)
    def rb_insert_fixup(self, node):
        while node.p.color=='red':       # if node.p.color is black, the property of rbtree still exist, no operation needed
            # node指针总是向上两层(因为node的父亲是红，而根是黑，所以node总能向上两层)
            # 最坏情况node会到根节点，根节点p指针指向nil，其颜色为黑，也会停止循环
            father = node.p
            if father is father.p.left:
                uncle = father.p.right
                if uncle.color == 'red':        # case 1
                    father.color = uncle.color = 'black'
                    father.p.color = 'red'          # maintain black-height equal property
                    node = father.p         # because this node color change to red, maybe it will destory rule
                    continue
                # only after case1 operation, case2 and case3 may happen
                elif father.right is node:      # case 2, node is right child of it's parent
                    node = father
                    self.left_rotate(node)      # left rotate to case 3
                # case 3, node is left child of it's parent
                node.p.color = 'black'
                node.p.p.color = 'red'
                self.right_rotate(node.p.p)
                # after case2 and case3, the loop condition will not satisified to quit
            else:   # node.p is node.p.p.right
                uncle = father.p.left
                if uncle.color == 'red':        # case 1
                    father.color = uncle.color = 'black'
                    father.p.color = 'red'
                    node = father.p
                    continue
                elif father.left is node:       # case 2
                    node = father
                    self.right_rotate(node)
                node.p.color = 'black'          # case 3
                node.p.p.color = 'red'
                self.left_rotate(node.p.p)
        self.root.color = 'black'       # here root cannot be nil

    # search
    def rb_search(self, key):
        current = self.root
        while current is not self.nil:
            if current.key == key:
                break
            elif current.key > key:
                current = current.left
            else:
                current = current.right
        return current
    # remove
    def rb_transplant(self, u, v):      # transplant v to u
        # absolutely transplant, just need to change two pointer(eg: u.p.child and v.p)
        if u.p == self.nil:
            self.root = v
        elif u == u.p.left:
            u.p.left = v
        else:
            u.p.right = v
        v.p = u.p
    def rb_delete(self, node):
        origin_color = node.color
        if node.left is self.nil:
            new_node_in_origin_place = node.right
            self.rb_transplant(node, node.right)
        elif node.right is self.nil:
            new_node_in_origin_place = node.left
            self.rb_transplant(node, node.left)
        else:           # find node's postprocessor, copy postprocessor to this node then delete postprocessor
            min_node_in_right_tree = self.tree_minimum(node.right)       # this node doesn't have left child, so it's easy to delete it
            origin_color = min_node_in_right_tree.color             # what we truly deleted is min_node_in_right_tree
            new_node_in_origin_place = min_node_in_right_tree.right
            # if min_node_in_right_tree is child of node: first, it must be node's right child
            # and min_node_in_right_tree.left child is nil, we don't need to transplant it's right child to itself
            # because before and after all procedure, it's right child will still be it's right child
            print(min_node_in_right_tree.key)
            if min_node_in_right_tree.p is node:
                if new_node_in_origin_place is self.nil:    # code which in <<introduction to algorithms>> is quite confusing, i add a bool statement to make it clear
                    new_node_in_origin_place.p = min_node_in_right_tree
            else:
                self.rb_transplant(min_node_in_right_tree, new_node_in_origin_place)
                min_node_in_right_tree.right = node.right
                node.right.p = min_node_in_right_tree
            self.rb_transplant(node, min_node_in_right_tree)
            min_node_in_right_tree.left = node.left
            node.left.p = min_node_in_right_tree
            min_node_in_right_tree.color = node.color
        if origin_color == 'black':
            self.rb_delete_fixup(new_node_in_origin_place)
    def rb_delete_fixup(self, node):
        # two cases: node's brother is red
        #            node's brother is black: three cases: brother's two child is black
        #                                                  brother's left child is red and right child is black
        #                                                  brother's right child is red
        # for more information, see <<introduction to algorithms>>
        while node is not self.root and node.color == 'black':
            if node is node.p.left:
                brother = node.p.right
                if brother.color == 'red':      # case 1, after case 1, it can be case 2, 3, 4
                    brother.color = 'black'
                    node.p.color = 'red'
                    self.left_rotate(node.p)
                    brother = node.p.right
                # brother must be black now
                if brother.left.color == 'black' == brother.right.color:        # case 2, after case 2, it can be case 1, 2, 3, 4
                    brother.color = 'red'
                    node = node.p
                    continue
                if brother.left.color == 'red' and brother.right.color == 'black':      #  case 3, after this, it can only be case 4
                    brother.color = 'red'
                    brother.left.color = 'black'
                    self.right_rotate(brother)
                    brother = node.p.right
                if brother.right.color == 'red':                # case 4
                    brother.right.color = 'black'
                    brother.color = node.p.color
                    node.p.color = 'black'
                    self.right_rotate(node.p)
                    break
            else:
                brother = node.p.left
                if brother.color == 'red':      # case 1
                    brother.color = 'black'
                    node.p.color = 'red'
                    self.right_rotate(node.p)
                    brother = node.p.left
                if brother.left.color == 'black' == brother.right.color:        # case 2
                    brother.color = 'red'
                    node = node.p
                    continue
                if brother.left.color == 'black' and brother.right.color == 'red':      # case 3
                    brother.color = 'red'
                    brother.right.color = 'black'
                    self.left_rotate(brother)
                if brother.left.color == 'red':                         # case 4, after case 4, everything will be satisfied
                    brother.left.color = 'black'
                    brother.color = node.p.color
                    node.p.color = 'black'
                    self.right_rotate(node.p)
                    break
        node.color = 'black'
    def tree_minimum(self, node):
        current = node
        while current.left is not self.nil:
            current = current.left
        return current

    def _rb_height(self, current, black=False, level=0, l=None):
        level += 1
        if len(l) < level: l.extend([0 for i in range(len(l))])
        if black and current.color == 'black':
            l[level] += 1
        _rb_height(current.left, black=black, level=level, l=l)
        _rb_height(current.right, black=black, level=level, l=l)
    def rb_height(self, black=False):           # BFS
        l = [0]*10
        if self.root is self.nil:
            return 0
        self._rb_height(self.root.left, black=black, level=0, l=l)
        self._rb_height(self.root.right, black=black, level=0, l=l)
        for index, i in enumerate(l[::-1]):
            if i != 0:
                return index
    def print_tree(self):
        queue = [[self.root]]
        level = 0
        print('-'*50)
        while queue[level]:
            queue.append([])
            print('level({}):'.format(level), end=' ')
            for node in queue[level]:
                print('{}({})'.format(node.key, node.color[0]), end=',')
                if node.left is not self.nil:
                    queue[level+1].append(node.left)
                if node.right is not self.nil:
                    queue[level+1].append(node.right)
            level += 1
            print()
        print('-'*50)
if __name__ == '__main__':
    import random
    tree = RbTree()
    l = [8, 1, 0, 5, 6, 3, 7, 2, 4, 9]
    for i in l:
        tree.rb_insert(i)
    tree.print_tree()
    l = [8, 7, 3, 1, 5, 9, 4, 6, 0, 2]
    for i in [8, 7, 3, 1, 5, 9, 4, 6, 0, 2]:
        print('delete', i)
        tree.rb_delete(tree.rb_search(i))
        tree.print_tree()
