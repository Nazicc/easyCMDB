#encoding: utf-8

import logging
import time
import platform

import psutil

from utils import sysutils
from .base import BasePlugin

logger = logging.getLogger(__name__)

class Client(BasePlugin):

    def __init__(self, config, *args, **kwargs):
        super(Client, self).__init__(config, 'client', 60, *args, **kwargs)


    def make_msg(self):
        msg = {
            'type' : 'register',
            'content' : {
                'hostname' : sysutils.get_hostname(),
                'ip' : sysutils.get_ip_address(),
                'mac' : sysutils.get_mac_address(),
                'cpu' : psutil.cpu_count(),
                'mem' : psutil.virtual_memory().total,
                'platform' : platform.platform(),
                'arch' : platform.architecture()[0],
                'pid' : getattr(self.config, 'PID'),
                'time' : time.time(),
            }
        }
        logger.debug('msg msg: %s', msg)
        return msg
