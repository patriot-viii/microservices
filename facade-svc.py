#!/usr/bin/env python3
from flask import Flask, request, jsonify, make_response
import uuid, requests, random, json, atexit
from ast import literal_eval
import hazelcast

LOGGING_URL = 'http://localhost'
MESSAGES_URL = 'http://localhost'

HAZLECAST_CLIENT = hazelcast.HazelcastClient()
HAZLECAST_QUEUE = HAZLECAST_CLIENT.get_queue("messages-queue") 

app = Flask(__name__)

@app.route('/api/messages', methods=['GET'])
def api_messages_get():
    print('/api/messages GET')

    logging = requests.get(get_logging_url() + '/logging/messages')
    messages = requests.get(get_messages_url() + '/messages/messages')

    return create_response(logging, messages)

@app.route('/api/messages/<id>', methods=['GET'])
def api_messages_id_get(id):
    print('/api/messages/<id> GET', id)

    logging = requests.get(get_logging_url() + '/logging/messages/'+id)
    messages = requests.get(get_messages_url() + '/messages/messages/'+id)

    return create_response(logging, messages)

@app.route('/api/messages', methods=['POST'])
def api_messages_post():
    content = request.json
    print('/api/messages POST', content)    
    
    content['uuid'] = str(uuid.uuid4())
    logging = requests.post(get_logging_url() + '/logging/messages', json=content)

    messages = requests.Response()
    if HAZLECAST_QUEUE.offer(content).result():
        print("Produced {}".format(content))
        messages.status_code = 200
        messages._content = json.dumps({'uuid':content['uuid']}).encode()
    else:
        print("Failed to produce {}".format(content))
        messages.status_code = 500
        messages._content = json.dumps({'error':'Not produced'}).encode()
    
    return create_response(logging, messages)

def create_response(logging, messages):
    resp = {
        'logging':{
            'code':logging.status_code,
            'content':literal_eval(logging.text)
        },
        'messages':{
            'code':messages.status_code,
            'content':literal_eval(messages.text)
        },
    }
    return jsonify(resp)

def get_logging_url():
    return get_url(LOGGING_URL, ['9090', '9091', '9092'])

def get_messages_url():
    return get_url(MESSAGES_URL, ['10010', '10011'])

def get_url(base_url, available_ports):
    url = ''
    while True:
        try:
            url = base_url + ':' + random.choice(available_ports)
            r = requests.options(url)
            print(url, '- selected')
            break
        except Exception as ex:
            print(url, '- failed to establish a new connection')

    return url

def on_exit():
    HAZLECAST_CLIENT.shutdown()

atexit.register(on_exit)

if __name__ == '__main__':
    app.run(host='0.0.0.0')