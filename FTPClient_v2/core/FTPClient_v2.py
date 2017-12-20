#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import socket
import os


class FtpClient(object):
    def __init__(self):
        self.client = socket.socket()
        self.current_path = None

    def connent(self, ip_port):
        self.client.connect(ip_port)

    def authenticate(self):
        while True:
            choice = ('''任意键登录，q退出。。。''')
            if choice != 'q':
                username = input('username:')
                password = input('password:')
                auth_info = 'authenticate|%s|%s' % (username, password)
                self.client.send(auth_info)
                rst = self.client.recv(1024)
                if rst == 'OK':
                    self.current_path = '/home/%s' % username
                    return True
                else:
                    print('账号或密码错误，请重新输入或退出（q）..')
                    return False
            else:
                exit('退出FTP。。。')

    def interactive(self):
        if self.authenticate():
            msg = input('>>').strip()
            msg_info = msg.split(' ')
            action = msg_info[0]
            if hasattr(self, action):
                getattr(self, action)(msg_info)
            else:
                print('非法操作。。。（help）')

    def help(self):
        print('''
            help 帮助信息
            put filename 上传文件
            get filename 下载文件
            pwd 当前路径
            cd path 切换路径
            ls path 查看文件
        ''')

    def put(self, *args):
        topath = self.current_path
        if len(args) > 1:
            filepath = args[1]
            if os.path.isfile(filepath):
                filesize = len(filepath)
                put_info = '''put|%s|%s|%s''' % (filepath, topath, filesize)
                self.client.send(put_info.encode('utf-8'))
                flag_quota = self.client.recv(1024).decode('utf-8')
                if flag_quota == 'OK':
                    pass
                else:
                    print('配额不足。。')
                    return False
        else:
            print('put filename..... or  help')
            return False

    def get(self):
        pass

    def cd(self):
        pass

    def ls(self):
        pass

    def pwd(self):
        print(self.current_path)
