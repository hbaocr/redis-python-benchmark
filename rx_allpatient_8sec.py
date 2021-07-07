from typing import Sized
import redis
import base64
import random as rd
import time

redis = redis.Redis(
     host= 'localhost',
     port= '6379',username='default',password='p@ssw0rd')

st = time.time_ns()

while True:
    time.sleep(8)
    tmp = time.time_ns()
    print(f"--->period : {(tmp-st)//1000000} ms")
    st=tmp
    start = time.time_ns()
    data =redis.scan(match="*",count=64000)
    print(f"it take {(time.time_ns() -start)/1000000} ms  to load: {len(data[1])} msg, offset ={data[0]}")