#encoding: utf-8

import logging
import threading

import requests

logger = logging.getLogger(__name__)

class ENS(threading.Thread):

    def __init__(self, config, *args, **kwargs):
        super(ENS, self).__init__(*args, **kwargs)
        self.config = config
        self.name = 'ens'
        self.daemon = True


    def run(self):
        _config = self.config
        _queue = getattr(_config, 'QUEUE')
        while True:
            _msg = _queue.get_nowait()
            if _msg:
                self.dispatch(_msg)


    def dispatch(self, msg):
        _type = msg.get('type')
        _content = msg.get('content')
        # print(type(_content))
        _url = 'http://{host}:{port}/api/v1/{type}/{uuid}/'.format(
            host=getattr(self.config, 'HOST'),
            port=getattr(self.config, 'PORT'),
            type=_type,
            uuid=getattr(self.config, 'UUID'),
        )
        _response = requests.post(_url, json=_content)
        if _response.ok:
            logger.debug('semd msg success: %s, response: %s', msg, _response.json())
        else:
            logger.error('send msg error: %s', msg)

