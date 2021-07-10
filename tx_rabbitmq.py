from typing import Sized
import redis
import base64
import random as rd
import time
import pika
from pika.exchange_type import ExchangeType

def gen_fake_ppg_data(usrID,devID,timestamp):
    # create the array off 100 byte which val = 123
    data_size = 100
    #data = bytearray([123] * data_size)
    ppg = rd.randbytes(data_size)    
    sessionID = 1234
    r = f"usr:{usrID}:dev:{devID}:sid:{sessionID}:ppg:{base64.urlsafe_b64encode(ppg)}:tim:{timestamp}"
    return r



url="amqps://hynparma:PTe2P2sFmMVEEbD1rXc1xPOgKajGMBIT@snake.rmq2.cloudamqp.com/hynparma"
exchange_name_='CheckRedisBuff'
routing_key_='validtor.cmd'
params = pika.URLParameters(url)
connection = pika.BlockingConnection(params)
channelRMQ = connection.channel()
# 1. Declare exchange
channelRMQ.exchange_declare(exchange=exchange_name_,exchange_type=ExchangeType.direct,durable=True)


redis = redis.Redis(
     host= 'localhost',
     port= '6379',username='default',password='p@ssw0rd')

 
number_of_online_user = 500
timer_sec=1

msg_ttl_sec = 16
channel_trigger = "CHECK_COMMING_DATA"
workerID =1
batch_sequence=0

st = time.time_ns()
dt=0

while True:
    
    tmp =time.time_ns()
    print(f"period : {(tmp-st)//1000000} ms, delay ={dt/1.000}sec")
    st=tmp
    for i in range(number_of_online_user): # emulate 1000
        t = time.time_ns()
        key= gen_fake_ppg_data(usrID=i,devID=i,timestamp=t)
        redis.set(name=key,value=1,ex=msg_ttl_sec) # exp = 16 sec 

    #finish batch of pushing data to Redis
    msg_pub = f"workerID:{workerID}:packetSeq:{batch_sequence}"
    batch_sequence=batch_sequence+1
    #redis.publish(channel_trigger,msg_pub)
    print(routing_key_+" : "+msg_pub)
    channelRMQ.basic_publish(exchange=exchange_name_,routing_key=routing_key_,body=msg_pub)

    dt = timer_sec-(time.time_ns()-tmp)/1000000000.000
    if(dt <=0):
        dt=0

    time.sleep(dt) #try to make sure 1sec in period





