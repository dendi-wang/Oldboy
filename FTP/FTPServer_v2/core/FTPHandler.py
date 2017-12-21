#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
import socketserver
import os
from core import dbHelper
from conf import settings


class FTPHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        super(FTPHandler, self).__init__(request, client_address, server)
        self.acc_info = None
        self.name = None
        self.mydbHelper = None
        # self.mydbHelper = dbHelper()

    def handle(self):
        while True:
            msg = self.request.recv(1024).decode('utf-8')
            if not msg:
                break
            else:
                msg_data = msg.split('|')
                action = msg_data[0]
                if hasattr(self, action):
                    getattr(self, action)(msg_data)
                else:
                    print("--\033[31;1mWrong msg type:%s\033[0m--" % action)

    def authenticate(self, msg_data):
        username = msg_data[1]
        password = msg_data[2]
        self.mydbHelper = dbHelper.dbHelper(username)
        acc_info = self.mydbHelper.get_acc_data()
        print(acc_info['username'], acc_info['password'])
        if acc_info:
            if username == acc_info['username'] and password == acc_info['password']:
                if os.path.exists(acc_info['home']):
                    print('home path 已存在')
                    pass
                else:
                    os.makedirs(acc_info['home'])
                    print('创建成功')
                print('%s登录成功。。。', username)
                self.acc_info = acc_info
                self.request.send('OK'.encode('utf-8'))
            else:
                self.request.send('ERR'.encode('utf-8'))
        else:
            self.request.send('NOT'.encode('utf-8'))

    def get(self, msg_data):
        file_path = msg_data[1]
        real_file_path = '%s/%s' % (settings.BASE_DIR, file_path)
        filename = os.path.split(real_file_path)[1]
        if os.path.exists(real_file_path):
            filesize = len(real_file_path)
            file_info = 'OK|%s' % filesize
            self.request.send(file_info.encode('utf-8'))
            tmp_filesize = 0
            f = open(file_path, 'rb')
            while tmp_filesize <= filesize:
                data = f.read(1024)
                self.request.send(data)
                tmp_filesize += 1024
            f.close()

    def put(self, msg_data):
        filename = msg_data[1]
        topath = msg_data[2]
        filesize = int(msg_data[3])
        real_topath = '%s%s' % (settings.BASE_DIR, topath)
        if filesize < self.acc_info['quota']:
            self.request.send('OK'.encode('utf-8'))
            tmp_filesize = 0
            f = open(os.path.join(real_topath, filename), 'wb')
            while tmp_filesize <= filesize:
                if filesize - tmp_filesize >= 1024:
                    recv_size = 1024
                else:
                    recv_size = filesize - tmp_filesize
                data = self.request.recv(recv_size)
                f.write(data)
                f.flush()
            f.close()
            self.acc_info['quota'] = self.acc_info['quota'] - filesize
            self.mydbHelper.mod_acc(self.acc_info)
            return True
        else:
            self.request.send('ERR'.encode('utf-8'))
            print('配额不足。。。。')
            return False

    def ls(self, msg_data):
        path = msg_data[1]

    def cd(self, msg_data):
        pass

#
# server = socketserver.ThreadingTCPServer(('localhost', 10000), FTPHandle)
# server.serve_forever()
