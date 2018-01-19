#encoding: utf-8

import logging
import time
# time.time()返回1970/1/1日起的时间戳的（单位是秒）
from .base import BasePlugin

logger = logging.getLogger(__name__)

class Heartbeat(BasePlugin):

    def __init__(self, config, *args, **kwargs):
        super(Heartbeat, self).__init__(config, 'heartbeat', 10, *args, **kwargs)


    def make_msg(self):
        msg = {
            'type' : 'heartbeat',
            'content' : {
                'time' : time.time(),
            }
        }
        logger.debug('msg msg: %s', msg)
        return msg
