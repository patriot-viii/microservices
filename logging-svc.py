#!/usr/bin/env python3
from flask import Flask, request, jsonify, make_response
import hazelcast
import atexit
from consul_facade import consul_get_value, consul_service_register, consul_service_deregister
from service_utils import get_host_port

HAZLECAST_CLIENT = hazelcast.HazelcastClient()
HAZLECAST_MAP = HAZLECAST_CLIENT.get_map(consul_get_value("MAP_LOGGING"))

app = Flask(__name__)

@app.route('/logging/messages', methods=['GET'])
def logging_messages_get():
    print('/logging/messages GET')

    all = {}
    for key, value in HAZLECAST_MAP.entry_set().result():
        all[key] = value
    return jsonify(all)

@app.route('/logging/messages/<id>', methods=['GET'])
def logging_messages_id_get(id):
    print('/logging/messages/<id> GET', id)

    if HAZLECAST_MAP.contains_key(id).result():
        msg = HAZLECAST_MAP.get(id).result()
        return jsonify(msg=msg)
    else:
        return make_response(jsonify({'error':'Not Found'}), 404)

@app.route('/logging/messages/<id>', methods=['DELETE'])
def logging_messages_id_delete(id):
    print('/logging/messages/<id> DELETE', id)

    if HAZLECAST_MAP.contains_key(id):
        if HAZLECAST_MAP.delete(id):
            return '', 200
        else:
            make_response(jsonify({'error':'Can not delete'}), 500)
    else:
        return make_response(jsonify({'error':'Not Found'}), 404)
    
@app.route('/logging/messages', methods=['POST'])
def logging_messages_post():
    content = request.json
    print('/logging/messages POST', content)
    uuid = content['uuid']
    msg = content['msg']
    HAZLECAST_MAP.set(uuid, msg)

    return jsonify(uuid=uuid)

def on_exit():
    print('on exit')
    consul_service_deregister(app.name, port)
    HAZLECAST_CLIENT.shutdown()

atexit.register(on_exit)

if __name__ == '__main__':
    host, port = get_host_port()
    consul_service_register(app.name, host, port)

    app.run(host=host, port=port)