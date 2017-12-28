#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang

import select
import socket
import os
import queue
from conf import settings


class FTPServer(object):
    def __init__(self):
        self.FTPs = socket.socket()

    def connent(self, ip_port):
        self.FTPs.bind(ip_port)
        self.FTPs.listen(5)

    def interactive(self):
        inputs = [self.FTPs, ]
        outputs = []
        put_dict = {}
        cmd_queues = {}
        # message_queues = {}
        getfile_queues = {}
        # putfile_queues = {}
        while True:
            recv_size = 1024
            readable, writeable, exeptional = select.select(inputs, outputs, inputs)
            for s in readable:
                if s is self.FTPs:
                    conn, client_addr = self.FTPs.accept()
                    conn.setblocking(False)
                    inputs.append(conn)
                else:
                    try:
                        msg = s.recv(recv_size)
                        if msg:
                            if s not in put_dict:
                                msg_info = msg.decode('utf-8').strip().split('|')
                                action = msg_info[0]
                                if action == 'put':
                                    print(msg.decode('utf-8'))
                                    self.put(msg_info, put_dict, s)
                                elif action == 'get':
                                    print(msg.decode('utf-8'))
                                    self.get(getfile_queues, s, msg_info, outputs)
                            elif s in put_dict:
                                f = open(put_dict[s][0], 'ab')
                                if put_dict[s][2] != put_dict[s][1]:
                                    f.write(msg)
                                    put_dict[s][2] += len(msg)
                                f.close()
                            else:
                                print("收到来自[%s]的数据:" % s.getpeername()[0], msg)
                    except Exception as e:
                        print("客户端断开了", s, e)
                        if s in outputs:
                            outputs.remove(s)
                        inputs.remove(s)
                        if s in getfile_queues:
                            del getfile_queues[s]
            for s in writeable:
                try:
                    next_msg = getfile_queues[s].get_nowait()
                except queue.Empty:
                    outputs.remove(s)
                else:
                    s.send(next_msg)

            for s in exeptional:
                # print("handling exception for ", s.getpeername())
                inputs.remove(s)
                if s in outputs:
                    outputs.remove(s)
                s.close()
                del getfile_queues[s]

    def put(self, msg_info, put_dict, s):
        filename = msg_info[1]
        filesize = int(msg_info[2])
        home_path = '%s/home/' % settings.BASE_DIR
        file_path = os.path.join(home_path, filename)
        tmp_filesize = 0
        put_dict[s] = [file_path, filesize, tmp_filesize]

    def get(self, getfile_queues, s, msg_info, outputs):
        getfile_queues[s] = queue.Queue()
        file_path = msg_info[1]
        if os.path.exists(file_path):
            filesize = os.path.getsize(file_path)
            getfile_queues[s].put(('OK|%s' % str(filesize)).encode('utf-8'))
            f = open(file_path, 'rb')
            get_filesize = 0
            while get_filesize != filesize:
                data = f.read(1024)
                getfile_queues[s].put(data)
                get_filesize += len(data)
            f.close()
        else:
            getfile_queues[s].put('ERR|0'.encode('utf-8'))
        if s not in outputs:
            outputs.append(s)
