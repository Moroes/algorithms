from copy import copy
from random import randint
from time import time

class Node:
    def __init__(self, value=0.0):
        self.parent = None
        self.value = value
        self.childs = []
        self.index = 0

class Binomial:
    def __init__(self):
        self.head = {}
        self.minimum = None

    def insert(self, x, ind=0):
        index = ind
        new_node = x
        while index in self.head:
            if new_node.value < self.head[index].value:
                self.head[index].parent = new_node
                new_node.childs.append(self.head[index])
            else:
                new_node.parent = self.head[index]
                self.head[index].childs.append(new_node)
                new_node = self.head[index]
            new_node.index += 1
            del self.head[index]
            index += 1
        self.head[index] = new_node
        self.update_min()

    def update_min(self):
        minimum = float("inf")
        minimum_node = None
        for i in self.head.values():
            if min(minimum, i.value) == i.value:
                minimum_node = i
                minimum = i.value
        self.minimum = minimum_node

    def min(self):
        return self.minimum

    def merge(self, tree):
        tree2_keys = tree.head.keys()
        for i in tree2_keys:
            self.insert(tree.head[i], ind=i)
        self.update_min()

    def __repr__(self):
        return repr(self.head)

    def delete_min(self):
        if self.head:
            minimum = self.min()
            new_tree = copy(minimum.childs)
            for node in new_tree:
                node.parent = None
            del self.head[minimum.index]
            del minimum
            for node in new_tree:
                self.insert(node, node.index)
        self.update_min()

    def decrease_key(self, node, new_value):
        node.value = new_value
        while node.parent:
            if node.parent.value > node.value:
                temp = node.parent.value
                node.parent.value = node.value
                node.value = temp
                node = node.parent
            else:
                break
        self.update_min()

    def delete(self, node):
        self.decrease_key(node, -1.0*float('inf'))
        self.delete_min()
        self.update_min()

class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0


    def percUp(self,i):
        while i // 2 > 0:
          if self.heapList[i] < self.heapList[i // 2]:
             tmp = self.heapList[i // 2]
             self.heapList[i // 2] = self.heapList[i]
             self.heapList[i] = tmp
          i = i // 2

    def insert(self,k):
      self.heapList.append(k)
      self.currentSize = self.currentSize + 1
      self.percUp(self.currentSize)

    def percDown(self,i):
      while (i * 2) <= self.currentSize:
          mc = self.minChild(i)
          if self.heapList[i] > self.heapList[mc]:
              tmp = self.heapList[i]
              self.heapList[i] = self.heapList[mc]
              self.heapList[mc] = tmp
          i = mc

    def minChild(self,i):
      if i * 2 + 1 > self.currentSize:
          return i * 2
      else:
          if self.heapList[i*2] < self.heapList[i*2+1]:
              return i * 2
          else:
              return i * 2 + 1

    def delMin(self):
      retval = self.heapList[1]
      self.heapList[1] = self.heapList[self.currentSize]
      self.currentSize = self.currentSize - 1
      self.heapList.pop()
      self.percDown(1)
      return retval

    def min(self):
        return self.heapList[1]

    def buildHeap(self,alist):
      i = len(alist) // 2
      self.currentSize = len(alist)
      self.heapList = [0] + alist[:]
      while (i > 0):
          self.percDown(i)
          i = i - 1



# binomial_tree = Binomial()

# for w in range(500):
#     binomial_tree.insert(Node(randint(0, 100000)))

# bh = BinHeap()
# bh.buildHeap([9,5,6,2,3])

# print(bh.delMin())
# print(bh.delMin())
# print(bh.delMin())
# print(bh.delMin())
# print(bh.delMin())
# print(bh)

# binomial_tree.create_dot()

def analys():
    insert_time_b_heap = []
    find_time_b_heap = []
    delete_time_b_heap = []

    insert_time_bin_heap = []
    find_time_bin_heap = []
    delete_time_bin_heap = []

    degr_time_b = []
    degr_time_bin = []
    for i in range(3,6):
        N = pow(10,i)
        b = BinHeap()
        bin = Binomial()


        # insert
        start_insert_b = time()
        degr_time_b.append([])

        for j in range(N):
            st_time = time()
            if j == 200:
                # b.insert(randint(0,N))
                degr_time_b[i - 3].append(time() - st_time)
            b.insert(randint(0,N))

        insert_time_b = time() - start_insert_b
        insert_time_b_heap.append(insert_time_b)

        start_insert_bin = time()
        for j in range(N):
            bin.insert(Node(randint(0,N)))
        insert_time_bin = time() - start_insert_bin
        insert_time_bin_heap.append(insert_time_bin)

        # find min
        start_find_b = time()
        for j in range(N):
            b.min()
        find_time_b = time() - start_find_b
        find_time_b_heap.append(find_time_b)

        start_find_bin = time()
        for j in range(N):
            bin.min()
        find_time_bin = time() - start_find_bin
        find_time_bin_heap.append(find_time_bin)

        # delete min
        start_delete_b = time()
        for j in range(N):
            b.delMin()
        delete_time_b = time() - start_delete_b
        delete_time_b_heap.append(delete_time_b)

        start_delete_bin = time()
        for j in range(N):
            bin.delete_min()
        delete_time_bin = time() - start_delete_bin
        delete_time_bin_heap.append(delete_time_bin)



        # print("i =", i)
        # print("B insert=", insert_time_b)
        # print("Bin insert=", insert_time_bin)
        # print()
    print("insert_time_b_heap =",insert_time_b_heap)
    print("find_time_b_heap =",find_time_b_heap)
    print("delete_time_b_heap =", delete_time_b_heap) 
    print("insert_time_bin_heap =", insert_time_bin_heap)
    print("find_time_bin_heap =", find_time_bin_heap)
    print("delete_time_bin_heap =", delete_time_bin_heap)
    print(degr_time_b)

analys()