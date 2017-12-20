#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
import socketserver
import os
from core import dbHelper
from conf import settings


class FTPHandle(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            msg = self.request.recv(1024)
            if not msg:
                break
            else:
                msg_data = msg.split('|')
                action = msg_data[0]
                if hasattr(self, action):
                    getattr(self, action)(msg_data)
                else:
                    print("--\033[31;1mWrong msg type:%s\033[0m--" % action)

    def ftp_auth(self, msg_data):
        username = msg_data[1]
        password = msg_data[2]
        acc_info = dbHelper(username)
        if not acc_info:
            if username == acc_info['username'] and password == acc_info['password']:
                if os.path.exists(acc_info['home']):
                    pass
                else:
                    os.makedirs(acc_info['home'])
                print('登录成功。。。')
                self.request.send('OK'.encode('utf-8'))
            else:
                self.request.send('ERR'.encode('utf-8'))
        else:
            self.request.send('NOT'.encode('utf-8'))

    def get(self, msg_data):
        file_path = msg_data[1]

    def put(self, msg_data):
        pass

    def ls(self, msg_data):
        pass

    def cd(self, msg_data):
        pass


server = socketserver.ThreadingTCPServer(('localhost', 10000), FTPHandle)
server.serve_forever()
