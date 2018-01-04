#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang




import pika
import uuid


class RPCClient(object):
    def __init__(self, ip, port, username, password):
        self.task_id = 1
        self.recv_data = {}
        self.credentials = pika.PlainCredentials(username, password)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', self.credentials))
        self.channel = self.conn.channel()
        result = self.channel.queue_declare(exclusive=True)
        self.callback_queue = result.method.queue
        self.channel.basic_consume(self.on_response, no_ack=True,
                                   queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode('utf-8')
            self.recv_data[self.task_id][self.corr_id] = self.response
            # print(self.response.decode('utf-8'))

    def run(self, hosts, cmd):
        self.task_id += 1
        self.data = {}
        print('task id: %s' % self.task_id)
        self.response = None
        # self.corr_id = str(uuid.uuid4())
        self.channel.exchange_declare(exchange='direct_rpc', exchange_type='direct')
        for host in hosts:
            self.corr_id = host
            self.data[self.corr_id] = None
            self.recv_data[self.task_id] = self.data
            self.channel.basic_publish(exchange='direct_rpc',
                                       routing_key=host,
                                       properties=pika.BasicProperties(
                                           reply_to=self.callback_queue,
                                           correlation_id=self.corr_id,
                                       ),
                                       body=cmd)
            self.conn.process_data_events(time_limit=5)

    # def break_loop(self, host):
    #     self.response = '%s 失去连接。。' % host

    def check_task(self, id):
        for host, data in self.recv_data.get(int(id)).items():
            print('''%s:
            %s''' % (host, data))


    def interactive(self):
        flag = True
        while flag:
            cmd_info = input('>>')
            action = cmd_info.strip().split(' ')[0]
            if action == 'exit':
                flag = False
            elif action == 'run':
                cmd = cmd_info.strip().split('run')[1].split('--')[0].strip(' ').strip('"')
                hosts = cmd_info.strip().split('--hosts')[1].strip().split(' ')
                self.run(hosts, cmd)
            elif action == 'check_task':
                cmd = cmd_info.strip().split(' ')
                if len(cmd) == 2:
                    id = cmd[1]
                    self.check_task(id)
                else:
                    print('task id 不存在。。。')
            else:
                print('非法命令。。。')
