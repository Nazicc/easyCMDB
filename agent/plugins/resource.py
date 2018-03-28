#encoding: utf-8

import logging
import psutil
from .base import BasePlugin


logger = logging.getLogger(__name__)

class Resource(BasePlugin):

    def __init__(self, config, *args, **kwargs):
        super(Resource, self).__init__(config, 'resource', 60, *args, **kwargs)

    def make_msg(self):
        msg = {
            'type' : 'resource',
            'content' : {
                'cpu' : psutil.cpu_percent(),
                'mem' : psutil.virtual_memory().percent
            }
        }
        logger.debug('msg msg: %s', msg)
        return msg
