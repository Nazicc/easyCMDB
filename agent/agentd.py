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

parser = argparse.ArgumentParser(prog='agentd', add_help=False)
parser.add_argument('-H', '--host', dest='host', help='', nargs='+')
parser.add_argument('-P', '--port', dest='port', help='', nargs='+')
parser.add_argument('-V', '--verbose', dest='detail', help='', action='store_true')
args = parser.parse_args()

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

    config = gconf.Config

    HOST = args.host[0]
    PORT = args.port[0]
    PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
    PID = os.getpid()

    if args.detail:
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s - %(name)s - %(levelname)s:%(message)s',
            filename=os.path.join(PROJECT_PATH, 'logs', 'agentd.log'),
            filemode='w',
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
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
