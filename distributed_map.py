#!/usr/bin/env python3
import hazelcast
import string
import random

client = hazelcast.HazelcastClient()

my_map = client.get_map("distributed-map")

# Fill the map
for i in range(1000):
    value =  ''.join(random.choice(string.ascii_letters) for i in range(10))
    my_map.put(str(i), value)

print("Map size:", my_map.size().result())

client.shutdown()