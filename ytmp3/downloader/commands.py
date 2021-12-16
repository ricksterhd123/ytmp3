# not sure how do to this nicely so here goes
import time
from model.video import Video
from model.priorityQueue import *
from downloader import download

class Command:
    """
    Command handler
    """
    def __init__(self, priority_queue):
        """
        :param PriorityQueue priority_queue
        """
        self._priority_queue = priority_queue

    def add(self, URL):
        try:
            id = download(URL)
        except Exception as ex:
            return False
        else:
            videos = self._priority_queue.items()
            
            # search for video in the priority queue
            found = False
            for i in range(len(videos)):
                if videos[i].id == id:
                    self._priority_queue.heap_increase_key(i, time.localtime())
                    found = True
            
            # insert if not found
            if not found:
                self._priority_queue.insert_heap(Video(id))

            return True
