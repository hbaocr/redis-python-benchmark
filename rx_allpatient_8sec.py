from typing import Sized
import redis
import base64
import random as rd
import time

redis = redis.Redis(
     host= 'localhost',
     port= '6379',username='default',password='p@ssw0rd')

channel_trigger = "CHECK_COMMING_DATA"
sub_chanel = redis.pubsub()
sub_chanel.subscribe(channel_trigger)
st = time.time_ns()
dt=0
while True:
     message=sub_chanel.get_message()
     if message and not message['data'] == 1:
          tmp =time.time_ns()
          print(f"period : {(tmp-st)//1000000} ms")
          st=tmp

          message = message['data'].decode('utf-8')
          print("============>new comming trigger from worker: " + message)
        
          start = time.time_ns()
          data =redis.scan(match="*",count=64000)
          print(f"---------->it take {(time.time_ns() -start)/1000000} ms  to load: {len(data[1])} msg, offset ={data[0]}")
          time.sleep(5)
'''
st = time.time_ns()
dt=0
timer_sec =8# 8sec
while True:
     tmp =time.time_ns()
     print(f"period : {(tmp-st)//1000000} ms, delay ={dt/1.000}sec")
     st=tmp
  
     start = time.time_ns()
     data =redis.scan(match="*",count=64000)
     print(f"---------->it take {(time.time_ns() -start)/1000000} ms  to load: {len(data[1])} msg, offset ={data[0]}")
     dt = timer_sec-(time.time_ns()-tmp)/1000000000.000
     if(dt <=0):
        dt=0
     time.sleep(dt) #try to make sure 1sec in period

'''