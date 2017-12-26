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

    def authenticate(self):
        while True:
            choice = ('''任意键登录，q退出。。。''')
            if choice != 'q':
                username = input('username:')
                password = input('password:')
                auth_info = 'authenticate|%s|%s' % (username, password)
                self.client.send(auth_info.encode('utf-8'))
                rst = self.client.recv(1024).decode('utf-8')
                if rst.split('|')[0] == 'OK':
                    self.current_path = rst.split('|')[1]
                    return True
                else:
                    print('账号或密码错误，请重新输入或退出（q）..')
                    return False
            else:
                exit('退出FTP。。。')

    def interactive(self):
        if self.authenticate():
            while True:
                # print(self.current_path)
                msg = input('%s$' % os.path.basename(self.current_path.strip('/'))).strip().strip('.').strip()
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
            pwd 当前路径
            cd path 切换路径
            ls path 查看文件
        ''')

    def put(self, *args):
        args = args[0]
        if len(args) == 2:
            topath = self.current_path
            if len(args) > 1:
                filepath = args[1]
                filename = os.path.basename(filepath)
                if os.path.isfile(filepath):
                    filesize = os.path.getsize(filepath)
                    put_info = '''put|%s|%s|%s''' % (filename, topath, str(filesize))
                    self.client.send(put_info.encode('utf-8'))
                    print(put_info)
                    flag_quota = self.client.recv(1024).decode('utf-8')
                    print(flag_quota)
                    if flag_quota == 'OK':
                        f = open(filepath, 'rb')
                        send_size = 0
                        count = math.ceil(filesize / 1024)
                        tmp_count = 0
                        print('开始上传文件。。。大小%s' % str(filesize))
                        while send_size != filesize:
                            tmp_count += 1
                            data = f.read(1024)
                            self.client.send(data)
                            send_size += len(data)
                            sys.stdout.write('{0}/{1}\r'.format(tmp_count, count))
                            sys.stdout.flush()
                        f.close()
                    else:
                        print('配额不足。。')
                        return False
            else:
                print('put filename..... or help')
                return False
        else:
            print('输入有误。。。')
            return False

    def get(self, *args):
        args = args[0]
        if len(args) == 2:
            filename = args[1]
            filepath = os.path.join(self.current_path, filename)
            get_info = '''get|%s''' % filename
            self.client.send(get_info.encode('utf-8'))
            file_info = self.client.recv(1024).decode('utf-8')
            file_exist = file_info.split('|')[0]
            filesize = int(file_info.split('|')[1])
            real_filename = os.path.split(filepath)[1]
            down_path = os.path.join(settings.download_path, real_filename)
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

    def cd(self, *args):
        args = args[0]
        if len(args) == 2:
            path = args[1]
            cd_info = 'cd|%s' % path
            self.client.send(cd_info.encode('utf-8'))
            cd_flag = self.client.recv(1024).decode('utf-8')
            if cd_flag.split('|')[0] == 'OK':
                self.current_path = cd_flag.split('|')[1]
                return True
            else:
                print('没有权限或者路劲不存在。。')
                return False
        else:
            print('命令有误。。。')
            return False

    def ls(self, *args):
        args = args[0]
        if len(args) == 1:
            ls_info = 'ls|%s' % self.current_path
            self.client.send(ls_info.encode('utf-8'))
        else:
            ls_info = 'ls|%s' % args[1]
            self.client.send(ls_info.encode('utf-8'))
        rst = self.client.recv(1024).decode('utf-8')
        print(rst)
        return rst

    def pwd(self, *args):
        print(self.current_path)
        return True
