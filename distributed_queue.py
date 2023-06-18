#!/usr/bin/env python3
import hazelcast
import threading

client = hazelcast.HazelcastClient()

queue = client.get_queue("distributed-queue") 


def produce():
    for i in range(100):
        queue.offer("value-" + str(i))


producer_thread = threading.Thread(target=produce)

producer_thread.start()

producer_thread.join()

client.shutdown()