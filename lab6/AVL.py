from os import remove
from random import randint

from numpy import insert


class Node:

    def __init__(self,value, left = None, right = None, parent = None, height = None) -> None:
        self.left = left
        self.value = value
        self.right = right
        self.parent = parent
        self.height = height

    
class BinaryTree():
    def __init__(self) -> None:
        self.head = None
        
    def add(self, element):
        if self.head == None:
            self.head = Node(element)
        else:
            node = self.head
            while True:
                if element > node.value:
                    if node.right == None:
                        node.right = Node(element)
                        return node
                    else:
                        node = node.right
                else:
                    if node.left == None:
                        node.left = Node(element)
                        return node
                    else:
                        node = node.left


    def pre_order(self, node):
        if node:
            print(node.value)
            self.pre_order(node.left)
            self.pre_order(node.right)

    def find(self, item):
        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)
        



class AVL():
    head = None

    def pre_order(self, node):
        if node:
            print(node.value)
            self.pre_order(node.left)
            self.pre_order(node.right)

    def post_order(self, node):
        if node:
            self.post_order(node.left)
            self.post_order(node.right)
            print(node.value)

    def in_order(self, node):
        if node:
            self.in_order(node.left)
            print(node.value)
            self.in_order(node.right)

    # def add(self, element):
    #     if self.head == None:
    #         self.head = Node(element)
    #     else:
    #         node = self.head
    #         while True:
    #             if element > node.value:
    #                 if node.right == None:
    #                     node.right = Node(element, parent=node)
    #                     return node
    #                 else:
    #                     node = node.right
    #             else:
    #                 if node.left == None:
    #                     node.left = Node(element, parent=node)
    #                     return node
    #                 else:
    #                     node = node.left

    def height(self, node:Node):
        if node is None or node.height is None:
            return 0
        else:
            return node.height


    def bfactor(self, node:Node):
        return self.height(node.right) - self.height(node.left)

    def fixheight(self, node:Node):
        hl = self.height(node.left)
        hl = hl if hl else 0
        hr = self.height(node.right)
        hr = hr if hr else 0
        node.height = (hl if hl > hr else hr) + 1

    def rotateright(self, node:Node):
        q:Node = node.left
        node.left = q.right
        q.right = node
        self.fixheight(node)
        self.fixheight(q)
        print(q.value)
        return q

    def rorateleft(self, node:Node):
        p:Node = node.right
        node.right = p.left
        p.left = node
        self.fixheight(node)
        self.fixheight(p)
        print(p.value)
        return p

    def balance(self, p:Node):
        self.fixheight(p)
        if self.bfactor(p) == 2:
            if (self.bfactor(p.right) < 0):
                p.right = self.rotateright(p.right)
            return self.rorateleft(p)
        if self.bfactor(p) == -2:
            if self.bfactor(p.left) > 0:
                p.left = self.rorateleft(p.left)
            return self.rotateright(p)
        return p

    # def insert(self, element, p:Node):
    #     if self.head is None:
    #         self.head = Node(element)
    #         return self.head
    #     if p is None:
    #         p = Node(element)
    #         return p
    #     elif element < p.value:
    #         p.left = self.insert(element, p.left)
    #     else:
    #         p.right = self.insert(element, p.right)
    #     return self.balance(p)

    def insert(self, element):
        if self.head is None:
            self.head = Node(element)
            return self.head
        else:
            return self.insert_r(element, self.head)

    def insert_r(self, element, p:Node):
        # if self.head is None:
        #     self.head = Node(element)
        #     return self.head
        if p is None:
            p = Node(element)
            return p
        elif element < p.value:
            p.left = self.insert_r(element, p.left)
        else:
            p.right = self.insert_r(element, p.right)
        return self.balance(p)


    def findmin(self, node:Node): #поиск узла с минимальным ключом в дереве p 
        return self.findmin(node.left) if node.left else node

    def removemin(self, node:Node): # удаление узла с минимальным ключом из дерева p
        if node.left == 0:
            return node.right
        node.left = self.removemin(node.left)
        return self.balance(node)

    def remove(self, node:Node, element):
        if node is None:
            return 0
        if element < node.value:
            node.left = self.remove(node.left, element)
        elif element > node.value:
            node.right = self.remove(node.right, element)
        else:
            q:Node = node.left
            r:Node = node.right
            if not r:
                return q
            min:Node = self.findmin(r)
            min.right = self.removemin(r)
            min.left = q
            return self.balance(min)
        self.balance(node)


    def find(self, item):
        def recurse(node:Node):
            if node is None:
                return None
            elif item == node.value:
                return node.value
            elif item < node.value:
                return recurse(node.left)
            else:
                return recurse(node.right)

        
def analys():
    for i in range(10):
        for j in range(20):
            if j < 10:
                arr = [[randint(0, 1e+6)] for el in range(pow(2, 10 + i))]
            else:
                arr = [el for el in range(pow(2, 10 + i))]
            

# analys()

a = AVL()

arr = list(randint(1, 30) for i in range(10))

print(arr)

for i in arr:
    a.insert(i)


# print(a.head.right.right.value)
print("--------")
a.pre_order(a.head)
a.remove(a.head, arr[4])
print("--------")
a.post_order(a.head)
print("--------")
a.in_order(a.head)

