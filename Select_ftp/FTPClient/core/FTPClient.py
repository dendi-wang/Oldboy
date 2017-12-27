#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import os
import socket, time

from conf import settings


class FTPClient(object):
    def __init__(self, ip_port):
        self.client = socket.socket()
        self.conn = self.client.connect(ip_port)

    def auth(self, userInfo):
        self.client.send(userInfo)
        rst = self.client.recv(1024)
        return rst

    def download(self, filepath):
        # conn, addr = self.FTPs.accept()
        print(filepath)
        self.client.send(str(filepath).encode('utf-8'))
        filesize = self.client.recv(1024).decode(encoding='utf-8')
        filename = os.path.split(filepath)[1]
        down_path = os.path.join(settings.download_path, filename)
        flag = True
        tmp_filesize = 0
        f = open(down_path, 'wb')
        print('开始下载文件....')
        # time.sleep(5)
        while flag:
            data = self.client.recv(1024)
            f.write(data)
            f.flush()
            tmp_filesize += len(data)
            # print(tmp_filesize)
            if int(filesize) - tmp_filesize == 0:
                flag = False
        f.close()
        return True

    def upload(self, file_path):
        # conn, addr = self.FTPs.accept()
        # file_path = self.conn.recv(1024).fileInfo.decode(encoding='utf-8')
        file_name = os.path.split(file_path)[1]
        file_size = str(os.path.getsize(file_path))
        file_info = '%s|%s' % (file_name, file_size)
        self.client.send(file_info.encode())
        f = open(file_path, 'rb')
        tmp_size = 0
        flag = True
        print('开始上传文件。。。。')
        while flag:
            data = f.read(1024)
            self.client.send(data)
            tmp_size += len(data)
            # print(file_size, tmp_size)
            if tmp_size == int(file_size):
                flag = False
                f.close()
        return True

    def exec_cmd(self, cmd_user):
        # conn, addr = self.FTPs.accept()
        self.client.send(cmd_user.encode('utf-8'))
        print(cmd_user)
        data = self.client.recv(1024)
        print(data.decode(encoding='utf-8'))
