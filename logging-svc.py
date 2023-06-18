#!/usr/bin/env python3
from flask import Flask, request, jsonify, make_response
import hazelcast
import atexit

HAZLECAST_CLIENT = hazelcast.HazelcastClient()
HAZLECAST_MAP = HAZLECAST_CLIENT.get_map("messages-map")

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


def close_running_threads():
    HAZLECAST_CLIENT.shutdown()

atexit.register(close_running_threads)

if __name__ == '__main__':
    app.run(host='0.0.0.0')