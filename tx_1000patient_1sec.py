from typing import Sized
import redis
import base64
import random as rd
import time

redis = redis.Redis(
     host= 'localhost',
     port= '6379',username='default',password='p@ssw0rd')

 

def gen_fake_ppg_data(usrID,devID,timestamp):
    # create the array off 100 byte which val = 123
    data_size = 100
    #data = bytearray([123] * data_size)
    ppg = rd.randbytes(data_size)    
    sessionID = 1234
    r = f"usr:{usrID}:dev:{devID}:sid:{sessionID}:ppg:{base64.urlsafe_b64encode(ppg)}:tim:{timestamp}"
    return r




 
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
    redis.publish(channel_trigger,msg_pub)
    print(channel_trigger+" "+msg_pub)

    dt = timer_sec-(time.time_ns()-tmp)/1000000000.000
    if(dt <=0):
        dt=0

    time.sleep(dt) #try to make sure 1sec in period

