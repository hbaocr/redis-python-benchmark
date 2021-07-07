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
    
    r = f"u:{usrID}:d:{devID}:ppg:{base64.urlsafe_b64encode(ppg)}:t:{timestamp}"
    return r




 
number_of_online_user = 1000

st = time.time_ns()
while True:
    time.sleep(1)
    tmp =time.time_ns()
    print(f"period : {(tmp-st)//1000000} ms")
    st=tmp
    for i in range(number_of_online_user): # emulate 1000
        t = time.time_ns()
        key= gen_fake_ppg_data(usrID=i,devID=i,timestamp=t)
        redis.set(name=key,value=1,ex=16) # exp = 180 sec


