#encoding: utf-8

import logging
import threading
import time

logger = logging.getLogger(__name__)

class BasePlugin(threading.Thread):

    def __init__(self, config, name='plugin', interval=60, *args, **kwargs):
        super(BasePlugin, self).__init__(*args, **kwargs)
        self.config = config        
        self.name = name
        self.interval = interval
        self.daemon = True

    def run(self):
        _config = self.config
        _queue = getattr(_config, 'QUEUE')
        _interval = self.interval
        while True:
            _msg = self.make_msg()
            if _msg:
                _queue.put_nowait(_msg)
            time.sleep(_interval)

    def make_msg(self):
        return None
