import pickle
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

    def swap(self, a, b):
        self.__array[a], self.__array[b] = self.__array[b], self.__array[a]

    @abstractmethod
    def length(self):
        pass
    
    @abstractmethod
    def pop(self, i):
        pass

    @abstractmethod
    def insert(self, i, x):
        pass

    @abstractmethod
    def minimum_item(self):
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

    def min_heapify(self, i, heapsize):
        l = self.left(i)
        r = self.right(i)

        if l <= heapsize - 1 and self.A.index(l) < self.A.index(i):
            smallest = l
        else:
            smallest = i
        
        if r <= heapsize - 1 and self.A.index(r) < self.A.index(smallest):
            smallest = r

        if smallest != i:
            self.A.swap(smallest, i)
            self.max_heapify(smallest, heapsize)

    def build_min_heap(self):
        for i in range(math.floor(self.A.length() / 2), -1, -1):
            self.min_heapify(i, self.A.heapsize)

    def heapsort(self):
        self.build_max_heap()
        tempheap = self.A.heapsize
        for i in range(self.A.length() - 1, 0, -1):
            self.A.swap(i, 0)
            tempheap -= 1
            self.min_heapify(0, tempheap)

class PriorityQueue(Heap):
    """
    Priority queue based on binary heap
    """
    def heap_minimum(self):
        return self.A.index(0)

    def heap_extract_min(self):
        if self.A.heapsize < 0:
            raise Exception("heap underflow")

        maximum = self.A.index(0)
        # pop method?
        self.A.pop(0)
        self.A.heapsize = self.A.heapsize - 1
        self.min_heapify(0, self.A.heapsize)
        return maximum

    def heap_increase_key(self, i, key):
        if key < self.A.index(i).priority:
            raise Exception("new key is smaller than current key")

        array = self.A.items()
        array[i].priority = key
        while i > 0 and self.A.index(self.parent(i)) > self.A.index(i):
            self.A.swap(self.parent(i), i)
            i = self.parent(i)

    def insert_heap(self, key):
        self.A.heapsize = self.A.heapsize + 1
        # insert method?
        self.A.insert(self.A.heapsize - 1, self.A.minimum_item(key.id))
        self.heap_increase_key(self.A.heapsize - 1, key.priority)

def save(file, obj):
    """
    Save to pickle file
    """
    if type(obj) != PriorityQueue:
        raise TypeError("Expected type " + str(PriorityQueue) + ", got " + str(type(obj)) + " instead")
    pickle.dump(obj, file)

def load(file):
    """
    This is potentially insecure,
    can we do something about it?
    https://docs.python.org/3/library/pickle.html
    """
    obj = pickle.load(file)
    if type(obj) != PriorityQueue:
        raise TypeError("Expected type " + str(PriorityQueue) + ", got " + str(type(obj)) + " instead")
    return obj
