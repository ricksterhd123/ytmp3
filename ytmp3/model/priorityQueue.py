import math
from abc import ABC, abstractclassmethod, abstractmethod

class Items(ABC):
    def __init__(self, array):
        self.__array = array
        self.heapsize = len(array)

    @abstractmethod
    def index(self, i):
        pass

    @abstractmethod
    def items(self):
        pass

    @abstractmethod
    def gt(self, i, x):
        """
        is A[i] > x?
        """
        pass

    @abstractmethod
    def lt(self, i, x):
        """
        is A[i] < x?
        """
        pass

    @abstractmethod
    def length(self):
        pass
    
    @abstractmethod
    def pop(self, i):
        pass

    @abstractmethod
    def insert(self, i, x):
        pass

class Heap:
    """
    A binary heap
    """
    def __init__(self, A):
        self.A = A

    def parent(self, i):
        return math.floor((i-1)/2)

    def left(self, i):
        return 2*i + 1

    def right(self, i):
        return 2*i + 2

    def max_heapify(self, i, heapsize):
        l = self.left(i)
        r = self.right(i)

        if l <= heapsize - 1 and self.A.index(l) > self.A.index(i):
            largest = l
        else:
            largest = i
        
        if r <= heapsize - 1 and self.A.index(r) > self.A.index(largest):
            largest = r

        if largest != i:
            self.A.index(largest), self.A.index(i) = self.A.index(i), self.A.index(largest)
            self.max_heapify(largest, heapsize)

    def build_max_heap(self):
        for i in range(math.floor(self.A.length() / 2), -1, -1):
            self.max_heapify(i, self.A.heapsize)

    def heapsort(self):
        self.build_max_heap()
        tempheap = self.A.heapsize
        for i in range(self.A.length() - 1, 0, -1):
            self.A.index(i), self.A.index(0) = self.A.index(0), self.A.index(i)
            tempheap -= 1
            self.max_heapify(0, tempheap)

class PriorityQueue(Heap):
    """
    Priority queue based on binary heap
    """
    def heap_maxixmum(self):
        return self.A.index(0)

    def heap_extract_max(self):
        if self.A.heapsize < 0:
            raise Exception("heap underflow")

        maximum = self.A.index(0)
        # pop method?
        self.A.pop(0)
        self.A.heapsize = self.A.heapsize - 1
        self.max_heapify(0, self.A.heapsize)
        return maximum

    def heap_increase_key(self, i, key):
        if key < self.A.index(i):
            raise Exception("new key is smaller than current key")

        self.A.index(i) = key
        while i > 0 and self.A.index(self.parent(i)) < self.A.index(i):
            self.A.index(self.parent(i)), self.A.index(i) = self.A.index(i), self.A.index(self.parent(i))
            i = self.parent(i)

    def insert(self, key):
        self.A.heapsize = self.A.heapsize + 1
        # insert method?
        self.A.insert(self.A.heapsize - 1, -math.inf)
        self.heap_increase_key(self.A.heapsize - 1, key)
