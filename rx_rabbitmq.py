from typing import Sized
import redis
import base64
import random as rd
import time
import pika
from pika.exchange_type import ExchangeType

redis = redis.Redis(
     host= 'localhost',
     port= '6379',username='default',password='p@ssw0rd')

st=0
def callback(ch, method, properties, body):
    global st
    print(" [x] Received %r" % body.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)
    tmp =time.time_ns()
    print(f"period : {(tmp-st)//1000000} ms")
    st=tmp
    
    start = time.time_ns()
    data =redis.scan(match="*",count=64000)
    print(f"---------->it take {(time.time_ns() -start)/1000000} ms  to load: {len(data[1])} msg, offset ={data[0]}")



url="amqps://hynparma:PTe2P2sFmMVEEbD1rXc1xPOgKajGMBIT@snake.rmq2.cloudamqp.com/hynparma"
exchange_name_='CheckRedisBuff'
routing_key_='validtor.cmd'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channelRMQ = connection.channel()
# 1. Declare exchange
channelRMQ.exchange_declare(exchange=exchange_name_,exchange_type=ExchangeType.direct,durable=True)

#auto create the queue with unique name
args = { "x-max-length": 1}
result=channelRMQ.queue_declare(queue='',durable=False,exclusive=True,arguments=args)

queue_name = result.method.queue
#bind the queue to the exchange
channelRMQ.queue_bind(queue=queue_name,exchange=exchange_name_,routing_key=routing_key_)
print(' [*] wait data from '+ queue_name)



channelRMQ.basic_consume(queue=queue_name,on_message_callback=callback,auto_ack=False,exclusive=False)

channelRMQ.start_consuming()



