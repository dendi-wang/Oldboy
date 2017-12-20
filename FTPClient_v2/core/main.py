#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

from core import FTPClient
from conf import settings


def user_auth(cli):
    name = input('name:')
    password = input('password:')
    userInfo = '%s|%s' % (name, password)
    rst = cli.auth(userInfo.encode('utf-8'))
    if rst.decode(encoding='utf-8') == 'ok':
        return True
    else:
        print('用户名密码错误...')
        return False


def main():
    print('登录FTP...')
    cli = FTPClient.FTPClient(settings.IP_PORT)
    name = input('name:')
    password = input('password:')
    userInfo = '%s|%s' % (name, password)
    rst = cli.auth(userInfo.encode('utf-8'))
    # print(rst)
    if rst.decode(encoding='utf-8') == 'ok':
        print('登录成功。。')
        while True:
            print('''请选择你的操作:
            下载文件
            上传文件
            查看文件
            ''')
            choice = input('>>>')
            if choice == '下载文件':
                cli.client.send(b'download')
                filepath = input('请输入要下载文件完整路径:')
                cli.download(filepath)
            elif choice == '上传文件':
                cli.client.send(b'upload')
                filepath = input('请输入要上传文件完整路径:')
                cli.upload(filepath)
            elif choice == '查看文件':
                cli.client.send(b'exec_cmd')
                cmd = 'dir|%s' % name
                cli.exec_cmd(cmd)
            elif choice == 'q':
                exit('退出系统')
            else:
                pass
    else:
        print('用户名密码错误...')
