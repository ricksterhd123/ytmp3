"""
Data structure for a video
"""
import time
from priorityQueue import Items, PriorityQueue

class Video():
    def __init__(self, id, last_used=None):
        self._id = id
        if type(last_used) != time.struct_time:
            last_used = None
        self._last_used = last_used or time.localtime()

    @property
    def id(self):
        return self._id

    @property
    def priority(self):
        return self._last_used

    @priority.setter
    def priority(self, new):
        self._last_used = new

    def __lt__(self, other):
        if not isinstance(other, Video):
            raise TypeError("expected {0} but got {1} instead".format(type(Video), type(other)))
        return self.priority < other.priority

    def __gt__(self, other):
        if not isinstance(other, Video):
            raise TypeError("expected {0} but got {1} instead".format(type(Video), type(other)))
        return self.priority > other.priority

    def __eq__(self, other):
        if not isinstance(other, Video):
            raise TypeError("expected {0} but got {1} instead".format(type(Video), type(other)))
        return self.priority == other.priority

    def __le__(self, other):
        if not isinstance(other, Video):
            raise TypeError("expected {0} but got {1} instead".format(type(Video), type(other)))
        return self.priority < other.priority or self.priority == other.priority

    def __ge__(self, other):
        if not isinstance(other, Video):
            raise TypeError("expected {0} but got {1} instead".format(type(Video), type(other)))
        return self.priority > other.priority or self.priority == other.priority

class Videos(Items):
    def __init__(self):
        self._videos = []
        super().__init__(self._videos)

    def index(self, i):
        return self._videos[i]

    def items(self):
        return self._videos

    def length(self):
        return len(self._videos)

    def pop(self, i):
        self._videos.pop(i)

    def insert(self, i, x):
        if type(x) != Video:
            raise TypeError("Expected type " + str(Video) + ", got " + str(type(x)) + " instead")
        self._videos.insert(i, x)

    def minimum_item(self, id):
        return Video(id, time.localtime(0))

if __name__ == '__main__':    
    p = PriorityQueue(Videos())
    p.insert_heap(Video(2))
    time.sleep(2)
    p.insert_heap(Video(3))
    time.sleep(2)
    p.insert_heap(Video(4))
    print("heapsize before", p.A.heapsize)
    for x in p.A.items():
        print(x.id, x.priority)
    
    p.heap_increase_key(0, time.localtime())

    for x in p.A.items():
        print(x.id, x.priority)