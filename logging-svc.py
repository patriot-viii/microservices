#!/usr/bin/env python3
from flask import Flask, request, jsonify, make_response

LOCAL_HASH_TABLE = {}

app = Flask(__name__)

@app.route('/logging/messages', methods=['GET'])
def logging_messages_get():
    print('/logging/messages GET')
    return jsonify(LOCAL_HASH_TABLE)

@app.route('/logging/messages/<id>', methods=['GET'])
def logging_messages_id_get(id):
    print('/logging/messages/<id> GET', id)

    if id in LOCAL_HASH_TABLE:
        return jsonify(msg=LOCAL_HASH_TABLE[id])
    else:
        return make_response(jsonify({'error':'Not Found'}), 404)

@app.route('/logging/messages', methods=['POST'])
def logging_messages_post():
    content = request.json
    print('/logging/messages POST', content)
    uuid = content['uuid']
    msg = content['msg']
    LOCAL_HASH_TABLE[uuid] = msg

    return jsonify(uuid=uuid)


if __name__ == '__main__':
    app.run(host='0.0.0.0')