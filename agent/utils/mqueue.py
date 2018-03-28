#encoding: utf-8
from queue import Queue, Empty, Full
# Full是Queue队列满时，再向内put时报的ERROR类型
# Empty是Queue队列满时，再从中get时报的ERROR类型

class PyQueue(Queue):
    def put(self, item, block=True, timeout=None):
        try:
            super(PyQueue, self).put(item, block, timeout)
            return True
        except Full as e:
            return False

    def get(self, block=True, timeout=None):
        try:
            return super(PyQueue, self).get(block, timeout)
        except Empty as e:
            return None

    def qsize(self):
        return super(PyQueue, self).qsize()

            
Queue = PyQueue