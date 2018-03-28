#encoding: utf-8
import os
import argparse
import logging
import time

import gconf

from utils import fileutils, sysutils
from utils import mqueue
from plugins.ens import ENS
from plugins.client import Client
from plugins.heartbeat import Heartbeat
from plugins.resource import Resource

logger = logging.getLogger(__name__)


def main(config):
    ths = {}

    ths['ens'] = {'class' : ENS, 'threading': None}
    ths['client'] = {'class' : Client, 'threading': None}
    ths['heartbeat'] = {'class' : Heartbeat, 'threading': None}
    ths['resource'] = {'class' : Resource, 'threading': None}

    while True:
        for key, value in ths.items():
            if value['threading'] is None or not value['threading'].is_alive():
                logger.error('threading[%s] is dead and restart', key)
                value['threading'] = value['class'](config)
                value['threading'].start()
        time.sleep(3)



if __name__ == '__main__':

    parser = argparse.ArgumentParser(prog='agentd', add_help=False)
    parser.add_argument('-H', '--host', dest='host', help='', type=str)
    parser.add_argument('-P', '--port', dest='port', help='', type=int)
    parser.add_argument('-V', '--verbose', dest='detail', help='', action='store_true')
    args = parser.parse_args()

    config = gconf.Config

    HOST = args.host
    PORT = args.port
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    PID = os.getpid()

    log_level = logging.DEBUG if args.detail else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s:%(message)s',
        filename=os.path.join(PROJECT_PATH, 'logs', 'agentd.log'),
        filemode='w',
    )

    setattr(config, 'HOST', HOST)
    setattr(config, 'PORT', PORT)
    setattr(config, 'PROJECT_PATH', PROJECT_PATH)
    setattr(config, 'PID', PID)
    setattr(config, 'QUEUE', mqueue.Queue())

    PATH_UUID = os.path.join(PROJECT_PATH, 'UUID')
    UUID = fileutils.read_file(PATH_UUID)
    if not UUID:
        UUID = sysutils.get_uuid()
        fileutils.write_file(PATH_UUID, UUID)

    setattr(config, 'UUID', UUID)

    logger.info('agentd is starting...')
    logger.info('PID: %s', PID)
    logger.info('UUID: %s', UUID)

    main(config)
