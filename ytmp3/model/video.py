"""
Data structure for a video
"""
import time
import pickle
from priorityQueue import Items

class Video():
    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._last_used = time.localtime()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def priority(self):
        return self._last_used

class Videos(Items):
    def __init__(self):
        self._videos = []
        super(self, self._videos)

    def index(self, i):
        return self._videos[i].priority()

    def items(self):
        return self._videos

    def gt(self, i, x):
        if type(x) != Video:
            raise TypeError("Expected type " + str(Video) + ", got " + str(type(x)) + " instead")
        return self.index(i) > x

    def lt(self, i, x):
        if type(x) != Video:
            raise TypeError("Expected type " + str(Video) + ", got " + str(type(x)) + " instead")
        return self.index(i) < x

    def length(self):
        return len(self._videos)

    def pop(self, i):
        self._videos.pop(i)

    def insert(self, i, x):
        if type(x) != Video:
            raise TypeError("Expected type " + str(Video) + ", got " + str(type(x)) + " instead")
        self._videos.insert(i, x)

def save(file, obj):
    """
    Save to pickle file
    """
    if type(obj) != Videos:
        raise TypeError("Expected type " + str(Videos) + ", got " + str(type(obj)) + " instead")
    pickle.dump(obj, file)

def load(file):
    """
    This is potentially insecure,
    can we do something about it?
    https://docs.python.org/3/library/pickle.html
    """
    obj = pickle.load(file)
    if type(obj) != Videos:
        raise TypeError("Expected type " + str(Videos) + ", got " + str(type(obj)) + " instead")
    return obj
