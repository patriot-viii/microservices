#!/usr/bin/env python3
import hazelcast
import time


client = hazelcast.HazelcastClient()

queue = client.get_queue("bounded-queue") 

while True:
    try:
        head = queue.take().result()
        print("Consuming {}".format(head))
    except Exception as err:
        print(f"Consuming error: {err=}, {type(err)=}")
        break
    time.sleep(1)

client.shutdown()