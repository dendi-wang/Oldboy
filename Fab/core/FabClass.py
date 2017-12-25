#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import paramiko


class FabClient(object):
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password


    def exec_cmd(self, cmd):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.host, self.port, self.username, self.password)
        strin, strout, strerr = ssh.exec_command(cmd)
        rst, err = strout.read(), strerr.read()
        result = rst if rst else err
        print(result)
        ssh.close()
        return result

    def sftp(self):
        transport = paramiko.Transport(self.host, self.port)
        transport.connect(username=self.username, password=self.password)
        sftpClient = paramiko.SFTPClient.from_transport(transport)
        return transport, sftpClient

    def put_file(self, remotepath, localpath):
        transport, sftpClient = self.sftp()
        sftpClient.put(localpath, remotepath)
        transport.close()

    def get_file(self, remotepath, localpath):
        transport, sftpClient = self.sftp()
        sftpClient.get(remotepath=remotepath, localpath=localpath)
        transport.close()
