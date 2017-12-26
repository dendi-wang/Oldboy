#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
import sys
import threading

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sys.path.append(BASE_DIR)

from core.FabClass import FabClient
from conf import settings


# print(type(settings.HOSTS))

def interactive():
    FabClient.show_hosts()
    flag = True
    while flag:
        msg = input('>>>').strip()
        if msg == 'q':
            flag = False
        elif msg == 'help':
            FabClient.help()
        elif msg == 'show_hosts':
            FabClient.show_hosts()
        else:
            msg_info = msg.split(' ')
            action = msg_info[0]
            hosts = get_host_info(msg_info)
            threading_list = []
            if hosts:
                lock = threading.RLock()
                for host in hosts:
                    fabc = FabClient(*host)
                    if hasattr(fabc, action):
                        t = threading.Thread(target=getattr(fabc, action), args=(msg, lock))
                        threading_list.append(t)
                        t.start()
                    else:
                        print('非法操作。。。（help）')
                        continue
                for t in threading_list:
                    t.join()
            else:
                print('主机或主机组不存在。。。')


def get_host_info(msg_info):
    hosts = []
    if len(msg_info) >= 4:
        if msg_info[1] == '-G':
            for k, v in settings.HOSTS[msg_info[2]].items():
                hosts.append(v)
            return hosts
        elif msg_info[1] == '-H':
            hosts.append(settings.HOSTS[msg_info[2]][int(msg_info[3])])
            return hosts
        else:
            return False
    else:
        return False

#
# interactive()
