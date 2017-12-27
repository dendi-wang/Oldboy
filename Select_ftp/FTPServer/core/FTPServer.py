import select
import socket
import os
import queue
from conf import settings

FTPs = socket.socket()
FTPs.bind(('localhost', 10000))
FTPs.listen(5)

inputs = [FTPs, ]
outputs = []
put_dict = {}
cmd_queues = {}
message_queues = {}
getfile_queues = {}
putfile_queues = {}
while True:
    recv_size = 1024
    readable, writeable, exeptional = select.select(inputs, outputs, inputs)
    for s in readable:
        if s is FTPs:
            conn, client_addr = FTPs.accept()
            conn.setblocking(False)
            inputs.append(conn)
        else:
            msg = s.recv(recv_size)
            msg_info = msg.decode('utf-8').strip().split('|')
            action = msg_info[0]
            if action == 'put':
                filename = msg_info[1]
                filesize = int(msg_info[2])
                home_path = '%s/home/' % settings.BASE_DIR
                file_path = os.path.join(home_path, filename)
                put_dict[s] = file_path
                if s in put_dict:
                    tmp_filesize = 0
                    if tmp_filesize != filesize:
                        f = open(put_dict[s], 'ab')
                        f.write(msg)
                        tmp_filesize += len(msg)
                else:
                    print("收到来自[%s]的数据:" % s.getpeername()[0], msg)
                if s not in outputs:
                    outputs.append(s)
            elif action == 'get':
                # print("收到来自[%s]的数据:" % s.getpeername()[0], msg)
                getfile_queues[s] = queue.Queue()
                file_path = msg_info[1]
                if os.path.exists(file_path):
                    filesize = os.path.getsize(file_path)
                    getfile_queues[s].put('OK|%s' % str(filesize))
                    f = open(put_dict[s], 'rb')
                    get_filesize = 0
                    while get_filesize != filesize:
                        data = f.read(1024)
                        getfile_queues[s].put(data)
                        get_filesize += len(data)
                    f.close()
                if s not in outputs:
                    outputs.append(s)
            else:
                print("客户端断开了", s)
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                del message_queues[s]
    for s in writeable:
        try:
            next_msg = message_queues[s].get_nowait()

        except queue.Empty:
            print("client [%s]" % s.getpeername()[0], "queue is empty..")
            outputs.remove(s)
        else:
            print("sending msg to [%s]" % s.getpeername()[0], next_msg)
            s.send(next_msg.upper())

    for s in exeptional:
        print("handling exception for ", s.getpeername())
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]
