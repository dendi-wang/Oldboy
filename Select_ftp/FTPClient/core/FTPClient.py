#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import socket
import os, sys, time, math

from conf import settings


class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()
        self.current_path = None

    def connent(self, ip_port):
        self.client.connect(ip_port)

    def interactive(self):
        # if self.authenticate():
        while True:
            # print(self.current_path)
            msg = input('>>')
            msg_info = msg.split(' ')
            action = msg_info[0]
            if hasattr(self, action):
                getattr(self, action)(msg_info)
            else:
                print('非法操作。。。（help）')

    def help(self, *args):
        print('''
            help 帮助信息
            put localfile 上传文件
            get remotefile 下载文件
        ''')

    def put(self, *args):
        args = args[0]
        if len(args) == 2:
            if len(args) > 1:
                filepath = args[1]
                filename = os.path.basename(filepath)
                if os.path.isfile(filepath):
                    filesize = os.path.getsize(filepath)
                    put_info = '''put|%s|%s''' % (filename, str(filesize))
                    self.client.send(put_info.encode('utf-8'))
                    f = open(filepath, 'rb')
                    tmp_size = 0
                    flag = True
                    print('开始上传文件。。。。')
                    while flag:
                        data = f.read(1024)
                        self.client.send(data)
                        tmp_size += len(data)
                        # print(file_size, tmp_size)
                        if tmp_size == int(filesize):
                            flag = False
                    f.close()
                    return True

            else:
                print('put filename..... ')
                return False
        else:
            print('输入有误。。。')
            return False

    def get(self, *args):
        args = args[0]
        if len(args) == 2:
            filepath = args[1]
            filename = os.path.basename(filepath)
            get_info = '''get|%s''' % filepath
            self.client.send(get_info.encode('utf-8'))
            file_info = self.client.recv(1024).decode('utf-8')
            print(file_info)
            file_exist = file_info.split('|')[0]
            filesize = int(file_info.split('|')[1])
            down_path = os.path.join(settings.download_path, filename)
            if file_exist == 'OK':
                tmp_filesize = 0
                f = open(down_path, 'wb')
                print('开始下载文件....%s,大小%s' % (filename, str(filesize)))
                count = math.ceil(filesize / 1024)
                tmp_count = 0
                while tmp_filesize != filesize:
                    if filesize - tmp_filesize >= 1024:
                        recv_size = 1024
                    else:
                        recv_size = filesize - tmp_filesize
                    tmp_count += 1
                    data = self.client.recv(recv_size)
                    f.write(data)
                    f.flush()
                    tmp_filesize += len(data)
                    # print('{0}%'.format(str(tmp_filesize/filesize*100)))
                    sys.stdout.write('{0}/{1}\r'.format(tmp_count, count))
                    sys.stdout.flush()
                    # time.sleep(1)
                f.close()
                print('下载文件完成')
            else:
                print(file_exist)
                return False
            return True
        else:
            print('输入有误。。。')
            return False
