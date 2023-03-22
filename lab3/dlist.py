from datetime import date
from enum import Flag
from operator import itemgetter
from platform import node
from random import randint
from numpy import sort
from scipy import rand


class Dlist:
    class Node:
        prev_node = None
        element = None
        next_node = None

        def __init__(self,element, prev_node = None, next_node = None) -> None:
            self.prev_node = prev_node
            self.element = element
            self.next_node = next_node

        def __add__(self, n):
            return self.element + n

        
    
    length = 0
    head = 0
    tail = 0

    def add(self, element, index = None):
        self.length += 1
        if not self.head:
            self.head = self.Node(element)
            return element

        elif not self.tail:
            self.tail = self.Node(element, self.head, None)
            self.head.next_node = self.tail
            return element

        elif not index:
            self.tail = self.Node(element, self.tail, None)
            self.tail.prev_node.next_node = self.tail
            return element

        else:
            if index > self.length:
                raise Exception("Index error")
            node = self.head
            for i in range(index):
                node = node.next_node
            tmp = node
            node = self.Node(element, tmp.element, node.next_node)
            node.prev_node = tmp
            tmp.next_node = node
            return node

    def _del(self, index, reverse = False):
        if index == 0:
            el = self.head.element
            self.head = self.head.next_node
            self.head.prev_node = None
            return el 

        elif index == self.length - 1:
            el = self.tail.element
            self.tail = self.tail.prev_node
            self.tail.next_node = None
            return el

        elif reverse:
            node = self.tail

            for i in range(self.length - 1, index, -1):
                node = node.prev_node

            el = node.element
            node.prev_node.next_node, node.next_node.prev_node = node.next_node, node.prev_node
            del node

            return el
        else:
            node = self.head

            for i in range(index):
                node = node.next_node

            el = node.element
            node.prev_node.next_node, node.next_node.prev_node = node.next_node, node.prev_node
            del node
            
            return el

    def delete(self, index):
        if index > self.length:
            raise Exception("Index error")
        self.length -= 1

        if self.head:
            if index >= self.length // 2:
                el = self._del(index, reverse = True)
                return el
            elif index < self.length // 2:
                el = self._del(index, reverse = False)
                return el

    def is_empty(self):
        return not self.length

    def sort(self):
        node = self.head
        for i in range(self.length-1):
            node2 = node
            for j in range(self.length-i-1):
                if node2.element > node2.next_node.element:
                    node2.element, node2.next_node.element = node2.next_node.element, node2.element

                node2 = node2.next_node
            node = node.next_node

    def __iter__(self):
        node = self.head

        while node:
            yield node.element
            node = node.next_node
    
    def __ne__(self, __o: Node) -> bool:
        return __o.element  




    

dlist = Dlist()

def analysis_1000():
    for i in range(1000):
        dlist.add(randint(-1000, 1000))
    summ = 0
    min_value = dlist.head.element
    max_value = dlist.head.element
    for i in dlist:
        summ += i
        if i < min_value:
            min_value = i
        if i > max_value:
            max_value = i
    avg_value = summ / dlist.length
    print(f"min = {min_value} max = {max_value} avg = {avg_value}")

def analysis_str():
    dlist_str = Dlist()
    for i in range(10):
        dlist_str.add(f"Строка {i + 1}")
    for i in dlist_str:
        print(i)
    print("Вставим элемент в середину:")
    dlist_str.add("Вставка----------------", 4)
    for i in dlist_str:
        print(i)
    print("Изъятие:")
    dlist_str.delete(2)
    for i in dlist_str:
        print(i)

dlist_struct = Dlist()
def analysis_struct():
    for i in range(100):
        class Strct:
            firstname = f"firstname {i}"
            lastname = f"lastname {i}"
            patronymic = f"patronymic {i}"
            date_of_birth = date(randint(1980, 2020), randint(1, 12), randint(1, 28))

            def __str__(self):
                return self.date_of_birth 

        dlist_struct.add(Strct)
    
    dlist_struct_new = Dlist()
    for i in dlist_struct:
        if i.date_of_birth < date(1990,1,1) or i.date_of_birth > date(2000,1,1):
            dlist_struct_new.add(i)
        
    for i in dlist_struct_new:
        print(i.date_of_birth)

        
def shake(dlist:Dlist):
    temp = dlist.head
    for i in enumerate(dlist):
        shake_index = randint(i[1] - 1, dlist.length - 1)
        el = i[0]
        if shake_index == dlist.length:
            el.element, dlist.tail.element = dlist.tail.element, el.element

        if shake_index == 0:
            continue

        node = dlist.head
        for j in range(shake_index):
            node = node.next_node
        
        el, node.element = node.element, el


# # print(a)

# for i in tst:
#     print(i)





# analysis_1000()
# analysis_str()

# analysis_struct()

tst = Dlist()

for i in range(100):
    tst.add(randint(0, 100))

# a = sorted(tst)
tst.sort()


for i in tst:
    print(i)

# print(a)

# flag = False
# for i in enumerate(tst):
#     if i != a[i[0]]:
#         flag = True

# print(flag)

print("shake:")
shake(tst)

for i in tst:
    print(i)