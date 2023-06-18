#!/usr/bin/env python3
from flask import Flask, jsonify, make_response
import hazelcast
import atexit, threading, time, json

HAZLECAST_CLIENT = hazelcast.HazelcastClient()
HAZLECAST_MAP = HAZLECAST_CLIENT.get_map("queue-map")
HAZLECAST_QUEUE = HAZLECAST_CLIENT.get_queue("messages-queue")

app = Flask(__name__)

@app.route('/messages/messages', methods=['GET'])
def messages_messages_get():
    print('/messages/messages GET')
    
    all = {}
    for key, value in HAZLECAST_MAP.entry_set().result():
        all[key] = value
    return jsonify(all)

@app.route('/messages/messages/<id>', methods=['GET'])
def messages_messages_id_get(id):
    print('/messages/messages/<id> GET', id)

    if HAZLECAST_MAP.contains_key(id).result():
        msg = HAZLECAST_MAP.get(id).result()
        return jsonify(msg=msg)
    else:
        return make_response(jsonify({'error':'Not Found'}), 404)

def on_exit():
    HAZLECAST_CLIENT.shutdown()
    CONSUMER_THREAD.join()

atexit.register(on_exit)

def consume():
    while True:
        try:
            item = HAZLECAST_QUEUE.take().result()            
            HAZLECAST_MAP.set(item['uuid'], item['msg'])
            print("Consuming {}".format(item))
        except Exception as err:
            print(f"Consuming error: {err=}, {type(err)=}")
            break
        time.sleep(1)

CONSUMER_THREAD = threading.Thread(target=consume)
CONSUMER_THREAD.start()

if __name__ == '__main__':
    app.run(host='0.0.0.0')