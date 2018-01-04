#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)
from conf import settings
from core import rpcServer

if __name__ == '__main__':
    client = rpcServer.RPCServer(settings.RABBITMQ_HOST, settings.RABBITMQ_PORT, settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
    client.run(settings.LOCALIP)
