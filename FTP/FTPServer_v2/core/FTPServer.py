#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import socket
import os

from conf import settings


class FTPServer(object):
    def __init__(self, ip_port):
        # self.IP_PORT = ip_port
        self.FTPs = socket.socket()
        self.FTPs.bind(ip_port)
        self.FTPs.listen(5)
        self.conn, self.user = self.FTPs.accept()

    def get_action(self):
        # conn, addr = self.FTPs.accept()
        action = self.conn.recv(1024).decode(encoding='utf-8')
        return action

    def upload(self):
        print('上传文件。。。。')
        # conn, addr = self.FTPs.accept()
        fileInfo = self.conn.recv(1024)
        # print(fileInfo)
        # print(type(fileInfo))
        filename = fileInfo.decode(encoding='utf-8').split('|')[0]
        filesize = fileInfo.decode(encoding='utf-8').split('|')[1]
        home_path = '%s/home/%s' % (settings.BASE_DIR, self.user)
        filepath = os.path.join(home_path, filename)
        flag = True
        tmp_filesize = 0
        f = open(filepath, 'wb')
        print('开始接收文件....')
        while flag:
            data = self.conn.recv(1024)
            f.write(data)
            f.flush()
            tmp_filesize += len(data)
            if int(filesize) - tmp_filesize == 0:
                flag = False
                print('接收文件完成。。。')
        f.close()

    def download(self):
        # conn, addr = self.FTPs.accept()
        file_path = self.conn.recv(1024).decode(encoding='utf-8')
        print('下载文件。。。。', file_path)
        # file_name = os.path.split(file_path)[1]
        file_size = os.path.getsize(file_path)
        self.conn.send(str(file_size).encode('utf-8'))
        f = open(file_path, 'rb')
        tmp_size = 0
        flag = True
        while flag:
            data = f.read(1024)
            self.conn.send(data)
            tmp_size += len(data)
            #print(tmp_size)
            if tmp_size == file_size:
                flag = False
        f.close()
        return True

    def exec_cmd(self):
        # conn, addr = self.FTPs.accept()
        cmd, user = self.conn.recv(1024).decode(encoding='utf-8').split('|')
        # user = self.conn.recv(1024).decode(encoding='utf-8').split('|')[1]
        home_path = '%s%shome%s%s' % (settings.BASE_DIR, settings.path_separator, settings.path_separator, user)
        cmd_x = '%s %s' % (cmd, home_path)
        # print(cmd_x)
        data = os.popen(cmd_x).read()
        # print(data)
        self.conn.send(data.encode('utf-8'))

    def auth(self):
        userInfo = self.conn.recv(1024).decode(encoding='utf-8')
        self.user = userInfo.split('|')[0]
        return userInfo

    def __del__(self):
        self.FTPs.close()
