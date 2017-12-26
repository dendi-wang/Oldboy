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
        self.current_path = None

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
                    print(action)
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
                self.current_path = '%s%s' % (settings.BASE_DIR, acc_info['home'])
                print(self.current_path, 'self.homepath')
                if os.path.exists(self.current_path):
                    print('home path 已存在')
                else:
                    os.makedirs(acc_info['home'])
                    print('创建成功')
                print('%s登录成功。。。' % username)
                self.acc_info = acc_info
                self.request.send(('OK|%s' % self.current_path).encode('utf-8'))
            else:
                self.request.send('ERR'.encode('utf-8'))
        else:
            self.request.send('NOT'.encode('utf-8'))

    def get(self, msg_data):
        file_path = msg_data[1]
        real_file_path = '%s/%s' % (self.current_path, file_path)
        print(real_file_path, 'real_file_path')
        filename = os.path.split(real_file_path)[1]
        if os.path.exists(real_file_path):
            filesize = os.path.getsize(real_file_path)
            file_info = 'OK|%s' % str(filesize)
            self.request.send(file_info.encode('utf-8'))
            tmp_filesize = 0
            f = open(real_file_path, 'rb')
            while tmp_filesize != filesize:
                data = f.read(1024)
                self.request.send(data)
                tmp_filesize += len(data)
            f.close()
        else:
            self.request.send('file in not exist|0'.encode('utf-8'))

    def put(self, msg_data):
        filename = os.path.split(msg_data[1])[1]
        topath = msg_data[2]
        filesize = int(msg_data[3])
        # real_topath = '%s%s' % (self.current_path, topath)
        if filesize < self.acc_info['quota']:
            print('quota', self.acc_info['quota'])
            self.request.send('OK'.encode('utf-8'))
            tmp_filesize = 0
            f = open(os.path.join(self.current_path, filename), 'wb')
            print('开始上传文件%s' % filename)
            while tmp_filesize != filesize:
                if filesize - tmp_filesize >= 1024:
                    recv_size = 1024
                else:
                    recv_size = filesize - tmp_filesize
                data = self.request.recv(recv_size)
                tmp_filesize += len(data)
                f.write(data)
                f.flush()
            f.close()
            print('上传文件%s完成。。' % filename)
            self.acc_info['quota'] = self.acc_info['quota'] - filesize
            self.mydbHelper.mod_acc(self.acc_info)
            return True
        else:
            self.request.send('ERR'.encode('utf-8'))
            print('配额不足。。。。')
            return False

    def ls(self, msg_data):
        path = msg_data[1]
        path_r = '%s/%s/' % (self.current_path, path)
        print(path_r)
        # print(path, path_r)
        if str(self.acc_info['home']) in str(path):
            print('ls %s' % path)
            rst = os.popen('ls %s' % path).read()
            print(rst)
        elif os.path.exists(path_r):
            rst = os.popen('ls %s' % path_r).read()
            print(rst)
        else:
            rst = 'Permission denied...'
            print(rst)
        if len(rst) == 0:
            rst = 'cmd in not output'
        self.request.send(rst.encode('utf-8'))
        return rst

    def cd(self, msg_data):
        path = msg_data[1]
        path_r = '%s/%s' % (self.current_path, path)
        if str(self.acc_info['home']) in str(path):
            data = os.popen('cd %s' % path).read()
            rst = '%s|%s' % ('OK', path)
            self.current_path = path
        elif os.path.exists(path_r):
            data = os.popen('cd %s' % path_r).read()
            rst = '%s|%s' % ('OK', path_r)
            self.current_path = path_r
        else:
            rst = 'Permission denied...'
        self.request.send(rst.encode('utf-8'))
        return rst

#
# server = socketserver.ThreadingTCPServer(('localhost', 10000), FTPHandle)
# server.serve_forever()
