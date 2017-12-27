#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
from core import FTPServer
from conf import settings


def user_auth(FTPs):
    userInfo = FTPs.auth()
    # print(userInfo)
    username = userInfo.split('|')[0]
    password = userInfo.split('|')[1]
    with open(settings.DB_PATH, 'r') as f:
        for line in f.readlines():
            # print(line)
            user = line.strip().split('|')[0]
            passwd = line.strip().split('|')[1]
            # print(user, password)
            if username == user and password == passwd:
                home_path = '%s/home/%s' % (settings.BASE_DIR, username)
                if os.path.exists(home_path):
                    pass
                else:
                    os.makedirs(home_path)
                return True
        else:
            return False


def main():
    print('FTPs已启动。。。。')

    while True:
        server = FTPServer.FTPServer(settings.IP_PORT)
        try:
            if user_auth(server):
                server.conn.send(b'ok')
                flag = True
                while flag:
                    action = server.conn.recv(1024).decode(encoding='utf-8')
                    print(action)
                    if action != 'q':
                        if hasattr(server, action):
                            # print(action, '---------------')
                            getattr(server, action)()
                    else:
                        flag = False
                        server.__del__()
            else:
                server.conn.send(b'err')
                server.__del__()
                print('密码错误')
        except ConnectionResetError:
            server.__del__()
            print('客户端非法关闭。。。。')
