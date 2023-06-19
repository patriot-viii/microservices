#!/usr/bin/env python3
from flask import Flask, jsonify, make_response
import hazelcast
import atexit, threading, time
from consul_facade import consul_get_value, consul_service_register, consul_service_deregister
from service_utils import get_host_port

HAZLECAST_CLIENT = hazelcast.HazelcastClient()
HAZLECAST_MAP = HAZLECAST_CLIENT.get_map(consul_get_value("MAP_MESSAGES"))
HAZLECAST_QUEUE = HAZLECAST_CLIENT.get_queue(consul_get_value("QUEUE_MESSAGES"))

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

def consume():
    while True:
        try:
            print("start consuming")
            item = HAZLECAST_QUEUE.take().result()
            print("Consumed {}".format(item))
            HAZLECAST_MAP.set(item['uuid'], item['msg'])
        except Exception as err:
            print(f"Consuming error: {err=}, {type(err)=}")
            break
        time.sleep(1)

CONSUMER_THREAD = threading.Thread(target=consume)
CONSUMER_THREAD.setDaemon(True)
CONSUMER_THREAD.start()

def on_exit():
    print('on exit')
    consul_service_deregister(app.name, port)
    HAZLECAST_CLIENT.shutdown()

atexit.register(on_exit)

if __name__ == '__main__':
    host, port = get_host_port()
    consul_service_register(app.name, host, port)

    app.run(host=host, port=port)