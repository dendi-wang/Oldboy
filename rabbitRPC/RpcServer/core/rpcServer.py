#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# Author: Harvey Wang
import pika
import os
import json


class RPCServer(object):
    def __init__(self, ip, port, username, password):
        self.credentials = pika.PlainCredentials(username, password)
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(ip, port, '/', self.credentials))
        self.channel = self.conn.channel()
        self.result = self.channel.queue_declare(exclusive=True)
        self.queue_name = self.result.method.queue

    def run(self, localip):
        self.channel.exchange_declare(exchange='direct_rpc',
                                      exchange_type='direct')
        self.channel.queue_bind(exchange='direct_rpc',
                                queue=self.queue_name,
                                routing_key=localip)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(self.on_request, queue=self.queue_name)
        print(" [x] Awaiting RPC requests")
        self.channel.start_consuming()

    def on_request(self, ch, method, props, body):
        self.cmd = body.decode('utf-8')
        print(self.cmd)
        data = os.popen(self.cmd).read()
        if len(data) == 0:
            data = '此命令没有输出'
        print(data)
        # response = {self.task_id: data}
        self.channel.basic_publish(exchange='',
                                   routing_key=props.reply_to,
                                   properties=pika.BasicProperties(correlation_id= \
                                                                       props.correlation_id),
                                   body=data
                                   )
        ch.basic_ack(delivery_tag=method.delivery_tag)
