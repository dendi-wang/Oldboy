#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import paramiko
from conf import settings


class FabClient(object):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    @staticmethod
    def show_hosts():
        print('''---------------主机列表---------------''')
        for group, host_info in settings.HOSTS.items():
            print(group)
            for index, host in host_info.items():
                print('%s. %s' % (index, host[0]))

    @staticmethod
    def help():
        print('''
        help : help info
        show_hosts : host list
        put file : put -H hostgroup host -file localfile remotepath or put -G hostgroup  -file localfile remotepath
        get file : get -H hostgroup host -file remotepath localfile or put -G hostgroup  remotepath  -file localfile
        exec_cmd : exec_cmd -H hostgroup host -shell 'cmd' or exec_cmd -G hostgroup  -shell 'cmd'
        ''')

    def exec_cmd(self, msg, lock):
        cmd = msg.split('-shell')[1]
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, self.port, self.username, self.password)
        strin, strout, strerr = ssh.exec_command(cmd)
        rst, err = strout.read(), strerr.read()
        result = rst if rst else err
        lock.acquire()
        print(self.host, ':', )
        print(result.decode('utf-8'))
        lock.release()
        ssh.close()
        return result

    def sftp(self):
        transport = paramiko.Transport(self.host, self.port)
        transport.connect(username=self.username, password=self.password)
        sftpClient = paramiko.SFTPClient.from_transport(transport)
        return transport, sftpClient

    def put(self, msg, lock):
        try:
            localpath, remotepath = msg.split('-file')[-1].strip().split(' ')
            transport, sftpClient = self.sftp()
            sftpClient.put(localpath, remotepath)
            transport.close()
            print('上传成功。。')
        except Exception as e:
            lock.acquire()
            print(self.host, e)
            lock.release()

    def get(self, msg, lock):
        try:
            remotepath, localpath = msg.split('-file')[-1].strip().split(' ')
            transport, sftpClient = self.sftp()
            sftpClient.get(remotepath=remotepath, localpath=localpath)
            transport.close()
            print('下载成功。。')
        except Exception as e:
            lock.acquire()
            print(self.host, e)
            lock.release()
