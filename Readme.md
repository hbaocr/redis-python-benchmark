## Redis

* start
```
docker-compose up -d    
```

* stop
```
docker-compose down    
```

* Redisinsignt  [link](http://127.0.0.1:8001/)

* Redis : 
  
  * host:`127.0.0.1`
  * usr: `default`
  * pass: `p@ssw0rd`


## Data

   Because redis doesn't support to get all value and keys at the same time. However it support get all the `key` by command `scan`, so we can embed all the data in the `key` and let the value is default `1` ( can be any, we don't care).

  The `key` format is : 
  ```
      key= f"u:{usrID}:d:{devID}:ppg:{base64.urlsafe_b64encode(ppg)}:t:{timestamp}"
      value = 1
  ```
  For `100byte` ppg : the `key` size is around `200byte` ===> to serve 1000 user and 1key/usr/1 sec and cache for 16 sec  :  16 * 1000 * 200 = 32*10^5 byte = 3.2 MByte

==> it took around `60-80ms` to retrieve all the `key` in redis




  By retrieving all  `key` ==> we can get all information from them.



* start tx :
  * `python3 tx_1000patient_1sec.py `

* read all the keys :
  * `python3 rx_allpatient_8sec.py `



## Benchmark for 800pat  : 1msg/1pat/1sec

* Packet size ( key size) : ~ 193 Byte
![keysize](KeySize.png)

* Get All `key` data from redis each 8 sec :
  * key_TTL = 16 sec ==> buffer 16 sec data/ patient
  * 800 pat  on line the same time ===> total key ~ 800*16 = 12800 msg
  * It take around 75-80ms to get all 12800 msg from redis
  * ![rx_800.png](rx_800.png)
* Memory analyse
  * ![800_user.png](800_user.png)
  

  


