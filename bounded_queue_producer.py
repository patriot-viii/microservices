#!/usr/bin/env python3
import hazelcast
import time


client = hazelcast.HazelcastClient()

queue = client.get_queue("bounded-queue") 

i = 0
while True:
    tail = "value-" + str(i)
    if queue.offer(tail).result():
        print("{} produced".format(tail))
    else:
        print("{} not produced".format(tail))
    i += 1
    time.sleep(1)

client.shutdown()